"""
    This module defines the Datamodel for the API input request
"""

__version__ = '0.1'
__author__ = 'suvrobaner@gmail.com'

from pydantic import BaseModel

class InputRequest(BaseModel):
    num_points: int
    response_value: int