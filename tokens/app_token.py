import requests
import json
import time

from .token import Token


class AppToken(Token):
    url = 'https://id.twitch.tv/oauth2/token'

    def __init__(self, client_id, client_secret):
        """
        Arguments:
            client_id -- str: Your client ID
            client_secret -- str: Your client secret
        """
        
        self.params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }

        self.update()