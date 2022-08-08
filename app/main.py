"""
This is the main module for starting the service -
This module defines the following usecases -

1. Configures Logger
2. Creates multiple middlewares
3. API versioning
4. Including Routers

"""

__version__ = '0.1'
__author__ = 'suvrobaner@gmail.com'

import time
from uuid import uuid4
import uvicorn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.middlewares.contextmiddleware import RequestContextMiddleware
from app.utils.logging import get_logger

from app.routers import polymerize_predict_router

_LOG_FILE = 'application.log'

logger = get_logger(name = 'app_log', filename = _LOG_FILE, write_file = False)

# This will be the main point of interaction to create all your API.
app = FastAPI()

# Adding all the relevant middlewares to FastAPI

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts = ["*"]
)

app.add_middleware(GZipMiddleware, minimum_size = 1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = False,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.add_middleware(RequestContextMiddleware)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info("Process Time: " + str(process_time))
    return response

@app.get("/")
async def healthcheck():
    return {"status": "alive"}

subapi = FastAPI()
subapi.include_router(polymerize_predict_router.router)
app.mount("/v1/polymerize_predict", subapi)
logger.info("Main app initialized for the service")

if __name__ == '__main__':
    pass
# uvicorn app.main:app --reload
# http://127.0.0.1:8000/docs

