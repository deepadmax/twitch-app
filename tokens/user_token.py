import requests
import json
import time

from .token import Token


"""This is not completed and should be set up to host a temporary Flask server
for authentication and retrieval of a user access token if none is found"""


class UserToken(Token):
    url = 'https://id.twitch.tv/oauth2/authorize'

    def __init__(self, client_id, redirect_uri, scope=''):
        """
        Arguments:
            client_id -- str: Your client ID
            redirect_uri -- str: Your registered redirect URI.
                This must exactly match the redirect URI registered.
            scope: either a regular list or a space-separated list, of scopes
        """

        if type(scope) is list:
            scope = ' '.join(scope)

        self.params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': scope
        }

        self.update()