import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    ADMIN_HOST_URL,
    LANDING_HOST_URL,
    API_HOST_URL
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_var('DJANGO_DATABASE_NAME'),
        'USER': get_env_var('DJANGO_DATABASE_USERNAME'),
        'PASSWORD': get_env_var('DJANGO_DATABASE_PASSWORD'),
        'HOST': get_env_var('DJANGO_DATABASE_HOST'),
        'PORT': '',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, "public")

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

X_FRAME_OPTIONS = 'DENY'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CORS

CORS_ORIGIN_WHITELIST = [
    'https://{}'.format(ADMIN_HOST_URL),
    'https://{}'.format(LANDING_HOST_URL)
]

# Sentry

sentry_sdk.init(
    dsn=get_env_var('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
