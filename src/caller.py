""" Class of API caller. """

import random
import requests
from auth import Auth

class APICaller:
    """ Class of API caller. """

    def __init__(self, config):
        """Instantiate on a Config"""
        self.config = config

    @property
    def _auth(self):
        auth = Auth(auth_config=self.config.AUTH)
        return auth.make_auth()


    @staticmethod
    def call_api_once(url, input_json, **auth):
        """ call API one time."""
        try:
            response = requests.post(url=url, json={"data": input_json}, **auth)
            if response.status_code == 200:
                # if return code 200 then the result can be dumped to a dict
                return response.json()['result']
            elif response.status_code == 401:
                exn_msg = f"Connection error: {url} - Token expired"
                print(exn_msg)
                raise Exception(exn_msg)
            else:
                exn_msg = f"Error: {response.text}"
                print(exn_msg)
                raise Exception(exn_msg)
        except Exception as exn:
            exn_msg = f"Error: {url} - {str(exn)}"
            print(exn_msg)
            raise Exception(exn_msg) from exn


    def call_api_batch(self):
        """ call API multiple time."""

        sample_n = int(self.config.SAMPLE_RATE * len(self.config.INPUT_JSON))
        print(f'\nSetup test cases: {sample_n} cases...')

        sample_keys = random.sample(self.config.INPUT_JSON.keys(), sample_n)
        print(f'Randomly selected cases: ["{sample_keys[0]}", ..., "{sample_keys[sample_n-1]}"]...')

        res_api_dct = {}
        expected_api_dct = {}
        for sample_key in sample_keys:
            res_api_0 = self.call_api_once(self.config.URL, self.config.INPUT_JSON[sample_key], **self._auth)
            if isinstance(res_api_0, dict):
                res_api = res_api_0[self.config.RETURN_KEY]
            else:
                res_api = res_api_0

            res_api_dct.update({sample_key: res_api})

            expected_api = self.config.EXPECTED_JSON.get(sample_key, 'ExpectedNotFound')
            expected_api_dct.update({sample_key: expected_api})

        return res_api_dct, expected_api_dct
