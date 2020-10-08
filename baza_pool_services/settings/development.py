from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# CORS

CORS_ORIGIN_WHITELIST = [
    'http://{}'.format(ADMIN_HOST_URL),
    'http://{}'.format(LANDING_HOST_URL)
]
