"""
    This module is for all utility functions
"""

__version__ = '0.1'
__author__ = 'suvrobaner@gmail.com'

import pickle
import pandas as pd

def writeToPickle(obj, filename):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file, protocol = pickle.HIGHEST_PROTOCOL)
        print('Written the file to {}'.format(filename))

def readFromPickle(filename):
    with open(filename, 'rb') as pickle_file:
        obj = pickle.load(pickle_file)
    return obj

def searchStringInDictKeys(obj, text):
    result = []
    for k, v in obj.items():
        if text in k:
            result.append(k)
    return result

def createDataLoader(input_data_dictionary):
    return pd.DataFrame(input_data_dictionary)
