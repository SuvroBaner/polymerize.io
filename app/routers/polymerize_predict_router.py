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

_LOG_FILE = 'application.log'
logger = get_logger(name = "app_log", filename = _LOG_FILE, write_file = False)

app_config = fetch_constants()

router = APIRouter(
    tags = ["Inference"],
    responses = {404: {'description': "Not Found"}}
)

@router.post("/predict_roughness")
async def predict_roughness(inputs: List[InputRequest], api_key: APIKey = Depends(get_api_key)):
    try:
        return inputs
    except Exception as err:
        logger.error(f"It failed with err : {err}")
        resp = {"status": False, "message": f"The response has failed due to {err}"}
        return resp


