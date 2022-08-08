"""
    This is the interface class for all the predictive model
"""

__version__ = '0.1'
__author__ = 'suvrobaner@gmail.com'

from abc import abstractmethod
from app.utils.singleton_factory import ModelSingleton

class Model(metaclass = ModelSingleton):

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def modelPredict(self):
        pass