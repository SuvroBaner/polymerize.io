"""
    Singleton class to instantiate the model just once
"""

__version__ = '0.1'
__author__ = 'suvrobaner@gmail.com'

from abc import ABCMeta

class ModelSingleton(ABCMeta):
    """This is a singleton metaclass for implementing singletone interfaces.
    author:andy
    Args:
        ABCMeta (_type_): _description_

    Returns:
        _type_: _description_
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ModelSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]