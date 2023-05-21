import requests
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
        response.raise_for_status()
        return response.json()["access_token"]

