""" Test That API. """


import json
import os
import random
import requests
import tempfile
import unittest

from collections import namedtuple
import datetime as dt

Config = namedtuple('Config', [
    'ID',
    'URL',
    'AUTH',
    'INPUT_JSON',
    'SAMPLE_RATE',
    'RETURN_KEY',
    'EXPECTED_JSON',
    'TYPE'
])

def make_auth(**kwargs):
    assert kwargs.get('auth_type', None) is not None, "auth_type should be provided"
    if kwargs['auth_type'] == 'Basic Auth':
        return basic_auth(**kwargs)
    elif kwargs['auth_type'] == 'Bearer Token':
        return bearer_token(**kwargs)
    else:
        raise NotImplementedError('Auth type is not implemented yet. Please contact author.')
        # raise Exception('Auth type is not implemented yet. Please contact author.')


def basic_auth(auth_type, username, password):
    """
    usernaem and password are environment variables.
    To save token in tmp file for security reason.
     """
    try:
        u = os.environ[username]
        p = os.environ[password]
        return {'auth': (u, p)}
    except Exception as exn:
        print(f'Error from basic_auth() - {str(exn)}')
        return None


def bearer_token(auth_type, auth_url, grant_type, client_id, client_secret, scope):
    """ Get Bearer Token for api. client_id and client_secret are environment variables."""

    print(f"\nTry authenticating user credentials...")

    try:
        id = os.environ[client_id]
        secret = os.environ[client_secret]

        payload = {
            'grant_type': grant_type,
            'client_id': id,
            'client_secret': secret,
            'scope': scope
            }

        r = requests.post(auth_url, data=payload).json()
        # t = r["access_token"]
        print(f"Successfully received a new token of {r['token_type']}, expires in {r['expires_in']}...")
        print(f"Please make sure your test ends by {dt.datetime.now() + dt.timedelta(seconds=r['expires_in'])}...")
        return {'headers': {"Authorization":f"Bearer {r['access_token']}"}}
    except Exception as exn:
        print(f'Error from bearer_token() - {str(exn)}')
        raise Exception(f'Error when trying to get {auth_type}.')


def make_config(config_json_path):

    def json_to_dct(json_path):
        with open(json_path, 'r', encoding='utf-8') as rjson:
            dct = json.load(rjson)
        return dct

    json_path = os.path.dirname(config_json_path)

    config = json_to_dct(config_json_path)
    input_json = json_to_dct(os.path.join(json_path, config['input_json']))
    expected_json = json_to_dct(os.path.join(json_path, config['expected_json']))

    return Config(
        config['id'],
        config['url'],
        make_auth(**config['auth']),
        input_json,
        config['sample_rate'],
        config['return_key'],
        expected_json,
        config['type']
        )


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


def call_api_batch(config):

    sample_n = int(config.SAMPLE_RATE * len(config.INPUT_JSON))
    print(f'\nSetup test cases: {sample_n} cases...')

    sample_keys = random.sample(config.INPUT_JSON.keys(), sample_n)
    print(f'Randomly selected cases: ["{sample_keys[0]}", ..., "{sample_keys[sample_n - 1]}"]...')

    res_api_dct = {}
    expected_api_dct = {}
    for sample_key in sample_keys:
        res_api = call_api_once(config.URL, config.INPUT_JSON[sample_key], **config.AUTH).json()['result'][config.RETURN_KEY]
        res_api_dct.update({sample_key: res_api})

        expected_api = config.EXPECTED_JSON.get(sample_key, 'ExpectedNotFound')
        expected_api_dct.update({sample_key: expected_api})

    return res_api_dct, expected_api_dct

# not used; experimenting
def token_to_tempfile(content):
    tmp_fp = tempfile.mkstemp(prefix='token_', text=True)
    with open(tmp_fp[0], 'w', encoding='utf-8') as fp:
        json.dump(content, fp)
    
    return tmp_fp
