from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "scollegetest",  # Nombre DB
        "USER": "root",  # Nombre usuario
        "PASSWORD": "cpce1901",  # Password
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {
            "sql_mode": "STRICT_TRANS_TABLES",
        },
    }
}


STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
MEDIA_DIRS = [BASE_DIR / "media/"]


# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True  # Usar TLS (Transport Layer Security) para cifrar la conexión
EMAIL_HOST_USER = "ircd.claudio@gmail.com"  # Reemplaza con tu dirección de correo electrónico de Gmail
EMAIL_HOST_PASSWORD = "ieiy rndj stsx vine"
