"""
    This is the model implentation class. 
    The model used will be linear regression
"""

__version__ = '0.1'
__author__ = 'suvrobaner@gmail.com'

from app.services.model_interface import Model
from app.utils.logging import get_logger
from app.utils.utility import readFromPickle
from app.utils.constants import fetch_constants

import numpy as np
from sklearn.linear_model import LinearRegression

_LOG_FILE = 'application.log'
logger = get_logger(name = "app_log", filename = _LOG_FILE, write_file = False)

app_config = fetch_constants()

class LinearRegressionModel(Model):
    
    def __init__(self, model_path):
        super(LinearRegressionModel, self).__init__()
        self.model_path = model_path
        
    def initialize(self):
        np.random.seed(101)
        self.model = readFromPickle(self.model_path)
    
    def modelPredict(self, data):
        predictions = self.model.predict(data)
        return predictions.tolist()