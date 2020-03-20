from django.conf import settings
from django.dispatch import receiver

from django.db.models.signals import post_save
# from celery.signals import task_prerun, task_recieved
from celery.task.control import revoke

from astrosat_tasks.celery import app as celery_app
from astrosat_tasks.conf import settings as app_settings
from astrosat_tasks.models import TaskSettings


@receiver(post_save, sender=TaskSettings)
def task_settings_post_save_handler(sender, **kwargs):
    print("changed TaskSettings")
    task_settings = kwargs.get("instance")
    if not task_settings.enable_celery:
        print("disabled")
        celery_app.control.purge()
        celery_app.control.disable_events()
    else:
        print("enabled")
        celery_app.control.enable_events()

# https://stackoverflow.com/a/54880615/1060339

# def task_prerun_handler(sender, **kwargs):
#     print("about to run a task wheee!")
#     if not app_settings.ASTROSAT_TASKS_ENABLE_CELERY:
#         task_id = kwargs["task_id"]
#         print(f"should cancel task {task_id}.")
#         celery_app.control.revoke(task_id, terminate=True)

# task_prerun.connect(
#     task_prerun_handler,
#     dispatch_uid="task_prerun_handler",
# )

# def task_recieved_handler(sender, **kwargs):
#     print("about to recieve a task wheee!")
#     if not app_settings.ASTROSAT_TASKS_ENABLE_CELERY:
#         request = kwargs["request"]
#         print(request)
#         celery_app.control.revoke(task_id, terminate=True)

# task_recieved.connect(
#     task_recieved_handler,
#     dispatch_uid="task_recieved_handler",
# )
