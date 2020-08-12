"""App configuration.
"""
from os import environ

DATABASE_URL = environ.get('DATABASE_URL')
HOST = environ.get('HOST', '0.0.0.0')
PORT = environ.get('PORT', 8000)  # noqa: WPS432
DEBUG = environ.get('DEBUG', True)
LIMIT_ROWS = 20
