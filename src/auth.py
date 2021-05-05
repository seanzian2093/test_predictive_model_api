""" auth class. """

import datetime as dt
import os
import requests

class Auth:

    def __init__(self, auth_config):
        """ Instantiate on a authentication config, i.e. Config.AUTH"""
        self.auth_config = auth_config

    def make_auth(self):

        assert self.auth_config.get('auth_type', None) is not None, "auth_type should be provided"

        if self.auth_config['auth_type'] == 'Basic Auth':
            return self.basic_auth(**self.auth_config)
        elif self.auth_config['auth_type'] == 'Bearer Token':
            return self.bearer_token(**self.auth_config)
        else:
            raise NotImplementedError('Auth type is not implemented yet. Please contact author.')


    @staticmethod
    def basic_auth(auth_type, username, password):
        """
        username and password are environment variables.
        To save token in tmp file for security reason.
        """
        try:
            u = os.environ[username]
            p = os.environ[password]
            return {'auth': (u, p)}
        except Exception as exn:
            print(f'Error from basic_auth() - {str(exn)}')
            # return None
            raise exn


    @staticmethod
    def bearer_token(auth_type, auth_url, grant_type, client_id, client_secret, scope):
        """ Get Bearer Token for api. client_id and client_secret are environment variables."""

        print(f"\nTry authenticating user credentials...")

        try:
            _id = os.environ[client_id]
            _secret = os.environ[client_secret]

            payload = {
                'grant_type': grant_type,
                'client_id': _id,
                'client_secret': _secret,
                'scope': scope
                }

            r = requests.post(auth_url, data=payload).json()
            print(f"Successfully received a new token of {r['token_type']}, expires in {r['expires_in']}...")
            print(f"Please make sure your test ends by {dt.datetime.now() + dt.timedelta(seconds=r['expires_in'])}...")
            return {'headers': {"Authorization":f"Bearer {r['access_token']}"}}
        except Exception as exn:
            print(f'Error from bearer_token() - {str(exn)}')
            raise Exception(f'Error when trying to get {auth_type}.')
