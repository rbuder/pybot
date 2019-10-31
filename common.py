#!/usr/bin/env python

from functools import wraps
from logging import getLogger
logger = getLogger(__name__)

def logWrap(func):
    @wraps(func)
    def log(*args, **kwargs):
        logger.debug('Function called: {}'.format(func.__name__))
        return func(*args, **kwargs)
    return log