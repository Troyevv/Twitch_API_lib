import requests
import pytz
import datetime
import json


class MissingParamsError(Exception):
    pass


class APIError(Exception):
    def __init__(self, message, status_code):
        super().__init__(f'API Error: Status_code: {status_code} - {message}')
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f'API Error: Status_code: {self.status_code} - {self.message}'


class TwitchAPI:
    def __init__(self, username, client_id, client_secret):
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self.get_token()

    def get_token(self):
        url = "https://id.twitch.tv/oauth2/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        headers = {
            "Accept": "application/json"
        }
        response = requests.post(url, data=data, headers=headers)
        return response.json()["access_token"]

    def get_stream_info(self):
        url = "https://api.twitch.tv/helix/streams?user_login=" + self.username
        headers = {
            "Authorization": "Bearer " + self.token,
            "Client-ID": self.client_id
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise APIError(response.status_code, "Invalid token")
        elif response.status_code == 404:
            raise APIError(response.status_code, "User not found")
        elif response.status_code == 429:
            raise APIError(response.status_code, "Too many requests")
        elif response.status_code == 500:
            raise APIError(response.status_code, "Server error")
        elif response.status_code == 400:
            raise APIError(response.status_code, "Bad request: The broadcaster_id query parameter is required")
        else:
            raise APIError(response.status_code, "Unknown error")

    def is_stream_online(self):
        response = self.get_stream_info()
        if len(response['data']) == 1:
            return True
        else:
            return False

    def channel_image(self):
        response = self.get_stream_info()
        if len(response['data']) == 1:
            return response['data'][0]['profile_image_url']
        else:
            return None

    def get_viewers_count(self):
        response = self.get_stream_info()
        if len(response['data']) == 1:
            return response['data'][0]['viewer_count']
        else:
            return None

    def get_title(self):
        response = self.get_stream_info()
        if len(response['data']) == 1:
            return response['data'][0]['title']
        else:
            return None

    def get_game(self):
        response = self.get_stream_info()
        if len(response['data']) == 1:
            return response['data'][0]['game_name']
        else:
            return None

    def get_started_at(self):
        response = self.get_stream_info()
        if len(response['data']) == 1:
            return response['data'][0]['started_at']
        else:
            return None

    def stream_duration(self, timezone):
        time_start = self.get_started_at()
        now = datetime.datetime.now(pytz.timezone(timezone))
        datetime_start = datetime.datetime.fromisoformat(time_start).replace(tzinfo=pytz.utc)
        datetime_start = datetime_start.astimezone(pytz.timezone(timezone))
        timestamp_diff = now - datetime_start
        duration = timestamp_diff - datetime.timedelta(microseconds=timestamp_diff.microseconds)
        return duration

    def get_broadcaster_id(self):
        response = self.get_stream_info()
        if len(response['data']) == 1:
            return response['data'][0]['broadcaster_id']
        else:
            return None

    def get_chatters(self):
        url = "https://api.twitch.tv/helix/chat/chatters"
        data = {
            "broadcaster_id": self.get_broadcaster_id(),
            "moderator_id": self.get_broadcaster_id()
        }
        headers = {
            "Authorization": "Bearer " + self.token,
            "Client-ID": self.client_id
        }
        response = requests.get(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise APIError(response.status_code, "The broadcaster_id query parameter is required\n"
                                                 "The ID in the broadcaster_id query parameter is not valid"
                                                 "\nThe moderator_id query parameter is required"
                                                 "\nThe ID in the moderator_id query parameter is not valid")
        elif response.status_code == 401:
            raise APIError(response.status_code, "Unauthorized: The access token is not valid")
        elif response.status_code == 403:
            raise APIError(response.status_code, "The user in the moderator_id query parameter is not one of the "
                                                 "broadcaster's moderators")
        else:
            raise APIError(response.status_code, "Unknown error")

    def create_clip(self):
        url = "https://api.twitch.tv/helix/clips"
        data = {
            "broadcaster_id": self.get_broadcaster_id()
        }
        headers = {
            "Authorization": "Bearer " + self.token,
            "Client-ID": self.client_id
        }
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 202:
            id_clip = response.json()['data'][0]['id']
            return id_clip
        elif response.status_code == 400:
            raise APIError(response.status_code, "The broadcaster_id query parameter is required")
        elif response.status_code == 401:
            raise APIError(response.status_code, "Unauthorized: The access token is not valid")
        elif response.status_code == 403:
            raise APIError(response.status_code, "The broadcaster has restricted the ability to capture clips to"
                                                 " followers and/or subscribers only")
        elif response.status_code == 404:
            raise APIError(response.status_code, "The broadcaster in the broadcaster_id query parameter must "
                                                 "be broadcasting live")

    def get_clips(self, id_clip=None, broadcaster_id=None, game_id=None, started_at=None, ended_at=None):
        if id_clip is None and broadcaster_id is None and game_id is None:
            raise MissingParamsError('The id_clip, broadcaster_id, or game_id query parameter is required')
        url = "https://api.twitch.tv/helix/clips"
        data = {}
        if id_clip is not None:
            data['id'] = id_clip
        if broadcaster_id is not None:
            data['broadcaster_id'] = broadcaster_id
        if game_id is not None:
            data['game_id'] = game_id
        if started_at is not None:
            data['started_at'] = started_at
        if ended_at is not None:
            data['ended_at'] = ended_at
        headers = {
            "Authorization": "Bearer " + self.token,
            "Client-ID": self.client_id
        }
        response = requests.get(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise APIError(response.status_code, "The broadcaster_id query parameter is required")
        elif response.status_code == 401:
            raise APIError(response.status_code, "Unauthorized: The access token is not valid")
        elif response.status_code == 403:
            raise APIError(response.status_code, "The broadcaster has restricted the ability to capture clips to"
                                                 " followers and/or subscribers only")

    def get_followers(self, user_id=None):
        url = "https://api.twitch.tv/helix/users/follows" + self.get_broadcaster_id()
        data = {}
        if user_id is not None:
            data['from_id'] = user_id
        headers = {
            "Authorization": "Bearer " + self.token,
            "Client-ID": self.client_id
        }
        response = requests.get(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise APIError(response.status_code, "The broadcaster_id query parameter is required")
        elif response.status_code == 401:
            raise APIError(response.status_code, "Unauthorized: The access token is not valid")
