#! /usr/bin/python3

from tta_utils import *

def test_that_api(config_fp):

    config = make_config(config_fp)
    print(f'\nStarted the testing for {config.ID}...')
    res = call_api_batch(config)
    assert res[0] == res[1], 'Your api testing did not pass. Please check the log for more info.'
    print(f'\nEnded the testing for {config.ID}...')
