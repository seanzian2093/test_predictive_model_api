""" Config for all entire testing process."""

import json
import os
from collections import namedtuple

Config = namedtuple('Config', [
    'ID', # Give a name for the API, informative
    'URL', # url to the endpoint function
    'AUTH', # arguments to construct an auth object
    'INPUT_JSON', # test cases in a JSON file
    'SAMPLE_RATE', # percentage of test cases to be tested
    'RETURN_KEY', # which key is the prediction returned
    'EXPECTED_JSON', # expected value in a JSON file
    'TYPE' # Type of the API, informative
])

def make_config(config_json_path):
    """ Config for all entire testing process."""

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
        # make_auth(**config['auth']),
        config['auth'],
        input_json,
        config['sample_rate'],
        config['return_key'],
        expected_json,
        config['type']
        )
