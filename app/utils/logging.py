"""
Logging Utilities
"""

__version__ = '0.1'
__author__ = 'suvrobaner@gmail.com'

import logging
import os
from logging import CRITICAL  # NOQA
from logging import DEBUG  # NOQA
from logging import ERROR  # NOQA
from logging import FATAL  # NOQA
from logging import INFO  # NOQA
from logging import NOTSET  # NOQA
from logging import WARN  # NOQA
from logging import WARNING  # NOQA
from typing import Optional

log_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

_default_log_level = log_levels["info"]
_log_format = '%(levelname)s : %(asctime)-15s %(filename)s:%(lineno)d %(funcName)-8s --> %(message)s'

def _get_library_name() -> str:
    return __name__.split(".")[0]

def get_logger(name: Optional[str] = None, 
                filename: Optional[str] = None, write_file = False) -> logging.Logger:
    """Return a logger with the specified name.
    This function can be used in dataset and metrics scripts.
    """
    if name is None:
        name = _get_library_name()

    logging.basicConfig(format = _log_format)
    logger = logging.getLogger(name)
    logger.setLevel(_default_log_level)

    if write_file:
        if filename is not None:
            formatter = logging.Formatter(_log_format)
            handler = _write_log_to_file(filename)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
    
    return logger

def _write_log_to_file(filename):
    if not os.path.exists('/tmp/app_logs'):
        os.makedirs('/tmp/app_logs')
    filename = '/tmp/app_logs/' + filename
    handler = logging.FileHandler(filename = filename)
    return handler