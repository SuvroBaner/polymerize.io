"""
This module enables all the routers -
"""

__version__ = '0.1'
__author__ = 'suvrobaner@gmail.com'

import os
import yaml
from typing import List

# APIRouter to break apart your api into routes
from fastapi import APIRouter, Path, Depends

# an application specific key like from query params, header, cookie
from fastapi.security.api_key import APIKey 

from app.utils.constants import fetch_constants
from app.utils.logging import get_logger
from app.middlewares.auth_apikey import get_api_key
from app.routers.datamodels import InputRequest
from app.services.generate_input import generateInputDistribution

_LOG_FILE = 'application.log'
logger = get_logger(name = "app_log", filename = _LOG_FILE, write_file = False)

app_config = fetch_constants()

router = APIRouter(
    tags = ["Inference"],
    responses = {404: {'description': "Not Found"}}
)

@router.post("/predict_roughness")
async def predict_roughness(inputs: InputRequest, api_key: APIKey = Depends(get_api_key)):
    try:
        target = 'roughness'
        results = generateInputDistribution(inputs.num_points, inputs.response_bin, target)
        return results
    except Exception as err:
        logger.error(f"It failed with err : {err}")
        resp = {"status": False, "message": f"The response has failed due to {err}"}
        return resp


