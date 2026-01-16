from .base import *

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
SWAGGER_USE_COMPAT_RENDERERS = False

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
