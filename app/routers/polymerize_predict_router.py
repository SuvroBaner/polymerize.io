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
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# an application specific key like from query params, header, cookie
from fastapi.security.api_key import APIKey 

from app.utils.constants import fetch_constants
from app.utils.logging import get_logger
from app.middlewares.auth_apikey import get_api_key
from app.routers.datamodels import InputRequest
from app.services.generate_input import generateInputDistribution
from app.services.polymerize_linear_regression import LinearRegressionModel
from app.utils.utility import createDataLoader

_LOG_FILE = 'application.log'
logger = get_logger(name = "app_log", filename = _LOG_FILE, write_file = False)

app_config = fetch_constants()

model_path = app_config['models']['linear_regression_model']
model_obj = LinearRegressionModel(model_path)
model_obj.initialize()
logger.info("The model is initialized from the path : {0}".format(model_path))

router = APIRouter(
    tags = ["Inference"],
    responses = {404: {'description': "Not Found"}}
)

@router.post("/predict_roughness")
async def predict_roughness(inputs: InputRequest, api_key: APIKey = Depends(get_api_key)):
    try:
        target = 'roughness'
        results = generateInputDistribution(inputs.num_points, inputs.response_bin, target)
        model_data = createDataLoader(results)
        predictions = model_obj.modelPredict(model_data)

        json_compatible_inp_sample_space = jsonable_encoder(results)
        json_compatible_predictions = jsonable_encoder(predictions)

        resp = {"status": True, 
                "message": "The response is successful", 
                "input_samplespace": json_compatible_inp_sample_space,
                "predictions": json_compatible_predictions}

        return JSONResponse(content = resp)
    
    except Exception as err:
        logger.error(f"It failed with err : {err}")
        resp = {"status": False, "message": f"The response has failed due to {err}"}
        return resp


