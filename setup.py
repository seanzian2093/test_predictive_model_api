#! /usr/bin/python3

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
setup(
    name='test_that_api',
    version='0.0.1',
    description='tta, Test That API. Test results from an api on a remote server or local host against expected results',
    author='Sean Zian',
    url='https://github.com/KusaiNeko',
    py_modules=['test_that_api', 'tta_utils'],
    package_dir={'': 'src'},
    license = "BSD",
    keywords = "API, Others",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
