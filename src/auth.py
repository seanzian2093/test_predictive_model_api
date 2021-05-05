""" auth class. """

import datetime as dt
import os
import requests

class Auth:
    """ Class for authentication."""

    def __init__(self, auth_config):
        """ Instantiate on an authentication config, i.e. Config.AUTH"""
        self.auth_config = auth_config


    def make_auth(self):
        """ A wrapper of all auth methods."""

        assert self.auth_config.get('auth_type', None) is not None, "auth_type should be provided"

        if self.auth_config['auth_type'] == 'Basic Auth':
            res = self.basic_auth(**self.auth_config)
        elif self.auth_config['auth_type'] == 'Bearer Token':
            res = self.bearer_token(**self.auth_config)
        else:
            raise NotImplementedError('Auth type is not implemented yet. Please contact author.')

        return res


    @staticmethod
    def basic_auth(auth_type, username, password):
        """username and password are environment variables."""
        assert auth_type == 'Basic Auth'
        try:
            _username = os.environ[username]
            _password = os.environ[password]
            return {'auth': (_username, _password)}
        except Exception as exn:
            exn_msg = f'Error from basic_auth() - {str(exn)}'
            print(exn_msg)
            raise Exception(exn_msg) from exn


    @staticmethod
    def bearer_token(auth_type, auth_url, grant_type, client_id, client_secret, scope):
        """ Get Bearer Token for api. client_id and client_secret are environment variables."""

        assert auth_type == 'Bearer Token'

        print(f"\nTry authenticating user credentials for {auth_type}...")

        try:
            _id = os.environ[client_id]
            _secret = os.environ[client_secret]

            payload = {
                'grant_type': grant_type,
                'client_id': _id,
                'client_secret': _secret,
                'scope': scope
                }

            res = requests.post(auth_url, data=payload).json()
            expires_at = dt.datetime.now() + dt.timedelta(seconds=res['expires_in'])

            print(f"Received a token of {res['token_type']}, expires in {res['expires_in']}...")
            print(f"Please complete test by {expires_at}...")
            return {'headers': {"Authorization":f"Bearer {res['access_token']}"}}
        except Exception as exn:
            exn_msg = f'Error from bearer_token() - {str(exn)}'
            print(exn_msg)
            raise Exception(exn_msg) from exn
