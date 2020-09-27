from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# CORS

CORS_ORIGIN_WHITELIST = [
    'http://{}'.format(ADMIN_HOST_URL)
]
