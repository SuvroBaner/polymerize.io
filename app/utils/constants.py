"""
    This module is there to read the constants file which will have model and other meta information
"""

__version__ = '0.1'
__author__ = 'suvrobaner@gmail.com'

import yaml

def fetch_constants(file_name = "app/resources/constants.yaml"):
    with open(file_name, 'r') as f:
        doc = yaml.safe_load(f)
    return doc