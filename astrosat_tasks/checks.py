import functools
import operator
import re
from itertools import chain

from django.conf import settings
from django.core.checks import register, Error, Tags

from . import APP_NAME
from .conf import app_settings

# apps required by astrosat_tasks
APP_DEPENDENCIES = [
    "astrosat",
    "django_celery_beat",
    "django_celery_results",
]


@register(Tags.compatibility)
def check_dependencies(app_configs, **kwargs):
    """
    Makes sure that all django app dependencies are met.
    (Standard python dependencies are handled in setup.py.)
    Called by `AppConfig.ready()`.
    """

    errors = []
    for i, dependency in enumerate(APP_DEPENDENCIES):
        if dependency not in settings.INSTALLED_APPS:
            errors.append(
                Error(
                    f"You are using {APP_NAME} which requires the {dependency} module.  Please install it and add it to INSTALLED_APPS.",
                    id=f"{APP_NAME}:E{i:03}",
                )
            )

    return errors


@register(Tags.compatibility)
def check_settings(app_configs, **kwargs):
    """
    Makes sure that some required settings are set as expected.
    """

    errors = []

    # obviously, a project that uses astrosat_tasks must connect to a broker
    celery_broker_url = getattr(settings, "CELERY_BROKER_URL", "")
    if re.match(r"^(.+)://(.+):(.+)@(.+):(\d+)$", celery_broker_url) is None:
        errors.append(
            Error(
                f"You are using {APP_NAME} which requires CELERY_BROKER_URL to be set properly."
            )
        )

    return errors


@register(Tags.compatibility)
def check_third_party_settings(app_configs, **kwargs):

    errors = []

    third_party_settings = [app_settings.CELERY_SETTINGS]

    for key, value in chain(*map(lambda x: x.items(), third_party_settings)):
        setting = getattr(settings, key, None)
        if setting != value:
            errors.append(
                Error(
                    f"You are using {APP_NAME} which requires {key} to be set to {value}."
                )
            )
    return errors
