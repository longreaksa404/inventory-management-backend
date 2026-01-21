from .base import *

DEBUG = True
ALLOWED_HOSTS = ["172.20.10.3", "localhost", "127.0.0.1"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

SWAGGER_USE_COMPAT_RENDERERS = False
