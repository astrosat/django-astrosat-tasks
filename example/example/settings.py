"""
Django settings for example project.
"""

import environ
import glob
import importlib
import os

from django.core.exceptions import ImproperlyConfigured
from django.utils.html import escape
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from astrosat.utils import DynamicSetting


PROJECT_NAME = "Example Project"
PROJECT_SLUG = slugify(PROJECT_NAME)

ROOT_DIR = environ.Path(__file__) - 2

env = environ.Env()
for env_file in glob.glob(ROOT_DIR(".env*")):
    try:
        env.read_env(env_file)
    except Exception as e:
        msg = f"Unable to read '{env_file}': {e}."
        raise ImproperlyConfigured(msg)

DEBUG = True

SECRET_KEY = "shhh..."

ROOT_URLCONF = "example.urls"

WSGI_APPLICATION = "example.wsgi.application"

ALLOWED_HOSTS = ["*"]

############
# Database #
############

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env("DJANGO_DB_HOST", default=""),
        "PORT": env("DJANGO_DB_PORT", default=""),
        "NAME": env("DJANGO_DB_NAME", default=""),
        "USER": env("DJANGO_DB_USER", default=""),
        "PASSWORD": env("DJANGO_DB_PASSWORD", default=""),
    }
}

########
# Apps #
########

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # api...
    "django_filters",
    "drf_yasg",
    "rest_framework",
    # tasks...
    "django_celery_beat",
    "django_celery_results",
    # astrosat...
    "astrosat",
    "astrosat_tasks",
    # this app...
    "example",
]

##############
# Middleware #
##############

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

#############
# Templates #
#############

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

##############
# Migrations #
##############

# hard-coded migration to set sites table
MIGRATION_MODULES = {"sites": "example.contrib.sites.migrations"}

SITE_ID = 1

#########
# Admin #
#########

ADMIN_URL = "admin/"

ADMIN_SITE_HEADER = f"{PROJECT_NAME} administration console"
ADMIN_SITE_TITLE = f"{PROJECT_NAME} administration console"
ADMIN_INDEX_TITLE = f"Welcome to the {PROJECT_NAME} administration console"

##################
# Authentication #
##################

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

#############
# Passwords #
#############

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

########################
# Internationalization #
########################

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [("en-us", _("American English")), ("en-gb", _("British English"))]
LOCALE_PATHS = [ROOT_DIR("locale")]

################
# Static files #
################

STATIC_URL = "/static/"
STATIC_ROOT = str(ROOT_DIR("static"))

#######
# API #
#######

REST_FRAMEWORK = {
    # TODO
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": escape("Enter 'Bearer <token>'"),
        },
        "Basic": {
            "type": "basic"
        },
    },
    "DOC_EXPANSION": "none",
    "OPERATIONS_SORTER": None,
    "TAGS_SORTER": "alpha",
    "DEFAULT_MODEL_RENDERING": "example",
}


#########
# Tasks #
#########

# ASTROSAT_TASKS_ENABLE_CELERY = DynamicSetting(
#     "astrosat_tasks.TaskSettings.enable_celery",
#     env("DJANGO_ASTROSAT_TASKS_ENABLE_CELERY", default=True),
# )

CELERY_BROKER_URL = "{transport}://{user}:{password}@{host}:{port}".format(
    transport=env("DJANGO_CELERY_BROKER_TRANSPORT", default="amqp"),
    port=env("DJANGO_CELERY_BROKER_PORT", default="5672"),
    host=env("DJANGO_CELERY_BROKER_HOST"),
    user=env("DJANGO_CELERY_BROKER_USER"),
    password=env("DJANGO_CELERY_BROKER_PASSWORD"),
)

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_TASK_SOFT_TIME_LIMIT = 60 * 5  # 5 minutes until SoftTimeLimitExceeded
CELERY_TASK_TIME_LIMIT = 60 * 25  # 25 minutes until worker is killed & replaced
# CELERY_TASK_COMPRESSION = gzip ?

# django_celery_results
CELERY_RESULT_BACKEND = "django-db"

# django_celery_beat
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

###########
# Logging #
###########

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[develop] %(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {"handlers": ["console"], "level": "DEBUG",},
    "loggers": {
        # when DEBUG is True, these loggers spit out _way_ too much information
        # so I'm increasing their levels
        "celery": {"level": "INFO"},
        "django.db.backends": {"level": "INFO"},
        "django.utils.autoreload": {"level": "INFO"},
        "environ.environ": {"level": "INFO"},
        "asyncio": {"level": "INFO"},
    },
}

#############
# Profiling #
#############

if DEBUG:

    # see "https://gist.github.com/douglasmiranda/9de51aaba14543851ca3"
    # for more tips about making django_debug_toolbar to play nicely w/ Docker

    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())

    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
    INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]

    INSTALLED_APPS += ["debug_toolbar", "pympler"]  # noqa F405
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "astrosat.middleware.JSONDebugToolbarMiddleware",
    ]  # noqa F405
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TEMPLATE_CONTEXT": True, "SHOW_COLLAPSED": True}
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ]
