import environ

from django.conf import settings
from django.utils.text import slugify

from astrosat.utils import DynamicSetting

from .. import APP_NAME

env = environ.Env()


PROJECT_NAME = getattr(settings, "PROJECT_NAME", "Django Astrosat TASKS")
PROJECT_SLUG = getattr(settings, "PROJECT_SLUG", slugify(PROJECT_NAME))

ASTROSAT_TASKS_ENABLE_CELERY = getattr(
    settings,
    "ASTROSAT_TASKS_ENABLE_CELERY",
    DynamicSetting(
        "astrosat_tasks.TaskSettings.enable_celery",
        env("DJANGO_ASTROSAT_TASKS_ENABLE_CELERY", default=True),
    ),
)

# required third party settings...
# (most of these are checked in checks.py)

CELERY_SETTINGS = {
    "CELERY_ACCEPT_CONTENT": ["json"],
    "CELERY_RESULT_SERIALIZER": "json",
    "CELERY_TASK_SERIALIZER": "json",
    # "CELERY_TASK_SOFT_TIME_LIMIT": 300,
    # "CELERY_TASK_TIME_LIMIT": 1500,
    "CELERY_RESULT_BACKEND": "django-db",
    "CELERY_BEAT_SCHEDULER": "django_celery_beat.schedulers.DatabaseScheduler",
}
