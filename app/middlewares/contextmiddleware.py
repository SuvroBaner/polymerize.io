"""
This module provides APIs to manage, store and access context-local state
The context class should be used to manage the current context in asynchronous frameworks
"""
__version__ = '0.1'
__author__ = 'suvrobaner@gmail.com'

from contextvars import ContextVar
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

'''
This abstract class that allows you to write ASGI middleware against a request / response inteface
rather that dealing with ASGI message directly.
'''

REQUEST_ID_CTX_KEY = "request_id"

_request_id_ctx_var: ContextVar[str] = ContextVar(REQUEST_ID_CTX_KEY, default = None)

def get_request_id() -> str:
    return _request_id_ctx_var.get()

class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware for generating uniqueid for each request
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        """
        call_next will receive the request as a parameter. This function will pass the request to the 
        corresponding path operation. Then it returns the response generated by the corresponding path operation
        """
        request_id = _request_id_ctx_var.set(str(uuid4()))
        response = await call_next(request)
        _request_id_ctx_var.reset(request_id)
        return response