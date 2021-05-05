""" Setup config for the package."""
import os
from setuptools import setup

def read(fname):
    """ Read README.md file to long_description. """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
setup(
    name='test_predictive_model_api',
    version='0.0.2',
    description='Test results from a predictive model api against expected results',
    author='Sean Zian',
    url='https://github.com/seanzian2093/test_predictive_model_api',
    py_modules=['auth', 'caller', 'config', 'main'],
    package_dir={'': 'src'},
    license = "MIT",
    keywords = "API, Predictive Model",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
