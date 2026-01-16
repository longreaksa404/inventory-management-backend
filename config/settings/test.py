# config/settings_test.py
from .settings import *

# Force Celery tasks to run synchronously in tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Use in‑memory email backend for tests
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
