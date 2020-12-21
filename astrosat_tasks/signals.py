# from django.conf import settings
# from django.dispatch import receiver

# from django.db.models.signals import post_save
# from celery.signals import task_prerun, task_recieved
# from celery.task.control import revoke

# from astrosat_tasks.celery import app as celery_app
# from astrosat_tasks.conf import settings as app_settings
# from astrosat_tasks.models import TaskSettings

# TODO: TRIED TO BE CLEVER AND AUTOMATICALLY SHUT-DOWN
# TODO: CELERY BASED ON THE VALUE OF TaskSettings.enable_celery
# TODO: BUT IT ISN'T QUITE THERE YET.  INSTEAD, I CAN USE THE
# TODO: @conditional_task DECORATOR AS WELL AS A CHECK IN
# TODO: task_detail_view AND run_task TO DISABLE _CERTAIN_ TASKS

# @receiver(post_save, sender=TaskSettings)
# def task_settings_post_save_handler(sender, **kwargs):
#     task_settings = kwargs.get("instance")
#     if not task_settings.enable_celery:
#         celery_app.control.purge()
#         celery_app.control.disable_events()
#     else:
#         celery_app.control.enable_events()

# @receiver(prerun_task...)
# def task_prerun_handler(sender, **kwargs):
#     if not app_settings.ASTROSAT_TASKS_ENABLE_CELERY:
#         task_id = kwargs["task_id"]
#         celery_app.control.revoke(task_id, terminate=True)

# @receiver(task_received...)
# def task_recieved_handler(sender, **kwargs):
#     if not app_settings.ASTROSAT_TASKS_ENABLE_CELERY:
#         celery_app.control.revoke(task_id, terminate=True)
