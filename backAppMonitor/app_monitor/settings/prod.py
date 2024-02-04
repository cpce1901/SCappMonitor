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

# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_RESULT_EXTENDED = True
CELERY_RESULT_BACKEND = "django-db"

# Correo de prueba
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True  # Usar TLS (Transport Layer Security) para cifrar la conexión
EMAIL_HOST_USER = "ircd.claudio@gmail.com"  # Reemplaza con tu dirección de correo electrónico de Gmail
EMAIL_HOST_PASSWORD = "ieiy rndj stsx vine"