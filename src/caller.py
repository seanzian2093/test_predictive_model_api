
import random
import requests
from auth import Auth

class APICaller:
    def __init__(self, config):
        """Instantiate on a Config"""
        self.config = config

    @property
    def _auth(self):
        auth = Auth(auth_config=self.config.AUTH)
        return auth.make_auth()


    @staticmethod
    def call_api_once(url, input_json, **auth):
        try:
            response = requests.post(url=url, json={"data": input_json}, **auth)
            if response.status_code == 200:
                return response
            elif response.status_code == 401:
                print(f"Connection error: {url} - Token expired")
                return {'rerult': "Token expired"}
            else:
                return {'rerult': f"{response.text}"}

        except Exception as e:
            print(f"Error: {url} - {str(e)}")
            raise Exception(f"Error: {url} - {str(e)}")


    def call_api_batch(self):

        sample_n = int(self.config.SAMPLE_RATE * len(self.config.INPUT_JSON))
        print(f'\nSetup test cases: {sample_n} cases...')

        sample_keys = random.sample(self.config.INPUT_JSON.keys(), sample_n)
        print(f'Randomly selected cases: ["{sample_keys[0]}", ..., "{sample_keys[sample_n - 1]}"]...')

        res_api_dct = {}
        expected_api_dct = {}
        for sample_key in sample_keys:
            res_api = self.call_api_once(
                self.config.URL, 
                self.config.INPUT_JSON[sample_key], 
                # **self.config.AUTH
                **self._auth
            ).json()['result'][self.config.RETURN_KEY]

            res_api_dct.update({sample_key: res_api})

            expected_api = self.config.EXPECTED_JSON.get(sample_key, 'ExpectedNotFound')
            expected_api_dct.update({sample_key: expected_api})

        return res_api_dct, expected_api_dct
