import os

from celery import Celery, shared_task

from django.apps import apps
from django.conf import settings

if not settings.configured:
    # PYTHONOPATH must include "server" for this to work
    # (see "run-queue.sh")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


app = Celery(settings.PROJECT_SLUG)

app.config_from_object("django.conf:settings", namespace="CELERY")
installed_apps = [app_config.name for app_config in apps.get_app_configs()]
app.autodiscover_tasks(lambda: installed_apps, related_name="tasks", force=True)

# NOTE: DO NOT FORGET THAT INVALID TASKS WILL NOT RAISE AN ERROR.
# NOTE: THEY WILL JUST NOT BE DISCOVERED; SO IF SOMETHING DOESN'T
# NOTE: SHOW UP IN THE BEAT DB SCHEDULER, THAT'S LIKELY TO BE THE CAUSE.
# NOTE: TO CHECK THIS JUST RUN `from <app> import tasks` FOR THE PROBLEMATIC
# NOTE: TASKS AND SEE IF ANY ERRORS ARE REPORTED


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


@app.task(bind=True)
def test_task(a, b):
    return_value = a + b
    return return_value
