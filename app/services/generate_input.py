"""
    This module generate the input space based on the response value and the number of points to be generated
"""

__version__ = '0.1'
__author__ = 'suvrobaner@gmail.com'

import numpy as np

from app.utils.logging import get_logger
from app.utils.constants import fetch_constants
from app.utils.utility import readFromPickle, searchStringInDictKeys

_LOG_FILE = 'application.log'
logger = get_logger(name = 'app_log', filename = _LOG_FILE, write_file = False)

app_config = fetch_constants()

distribution_stats = readFromPickle(app_config['stats']['input_distribution'])

def generateInputDistribution(num_points, y_bin, target):
    intervals = searchStringInDictKeys(app_config[target], y_bin)

    for interval in intervals:
        if 'start' in interval:
            start = int(app_config[target][interval])
        elif 'end' in interval:
            end = int(app_config[target][interval])
    
    final_distribution = {}
    for variable, metrics in distribution_stats[y_bin].items():
        mu = metrics[0]
        sigma = metrics[1]
        s = np.random.normal(mu, sigma, num_points)
        final_distribution[variable] = s
    
    return final_distribution