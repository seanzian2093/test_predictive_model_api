
""" Main function to call api in batch mode."""
from caller import APICaller
from config import make_config

def main(config_fp):
    """ main function to call api in batch mode."""

    config = make_config(config_fp)
    print(f'\nStarted the testing for {config.ID}...')
    api_caller = APICaller(config)
    res = api_caller.call_api_batch()
    assert res[0] == res[1], 'Your api testing did not pass. Please check the log for more info.'
    print(f'\nNo news is good news for {config.ID}...')
    print(f'\nCompleted the testing for {config.ID}...')
