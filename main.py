import requests
import pytz
import datetime
import json


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
        print(response.json())
        return response.json()["access_token"]

    def get_stream_info(self):
        url = "https://api.twitch.tv/helix/streams?user_login=" + self.username
        headers = {
            "Authorization": "Bearer " + self.token,
            "Client-ID": self.client_id
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(response.json())
            return response.json()
        elif response.status_code == 401:
            raise Exception("Invalid token")
        elif response.status_code == 404:
            raise Exception("User not found")
        elif response.status_code == 429:
            raise Exception("Too many requests")
        elif response.status_code == 500:
            raise Exception("Server error")
        elif response.status_code == 400:
            raise Exception("Bad request: The broadcaster_id query parameter is required")
        else:
            raise Exception("Unknown error")

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
            print(response.json())
            return response.json()
        elif response.status_code == 400:
            raise Exception("The broadcaster_id query parameter is required\n"
                            "The ID in the broadcaster_id query parameter is not valid"
                            "\nThe moderator_id query parameter is required"
                            "\nThe ID in the moderator_id query parameter is not valid")
        elif response.status_code == 401:
            raise Exception("Unauthorized: The access token is not valid")
        elif response.status_code == 403:
            raise Exception("The user in the moderator_id query parameter is not one of the broadcaster's moderators")
        else:
            raise Exception("Unknown error")