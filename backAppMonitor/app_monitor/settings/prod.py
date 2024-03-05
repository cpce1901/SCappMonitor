from .base import *

DEBUG = False

ALLOWED_HOSTS = ['164.92.64.11', 'www.energyconviction.cl', 'energyconviction.cl']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "scollegeprod",  # Nombre DB
        "USER": "cpce1901",  # Nombre usuario
        "PASSWORD": "cpce1901",  # Password
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {
            "sql_mode": "STRICT_TRANS_TABLES",
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'


