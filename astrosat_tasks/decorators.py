import functools

from .conf import app_settings


def conditional_task(task_fn):

    """
    A decorator for a task that only runs the task if celery is enabled
    """

    @functools.wraps(task_fn)
    def astrosat_task_wrapper(*args, **kwargs):
        if not app_settings.ASTROSAT_TASKS_ENABLE_CELERY:
            return None
        task_fn(*args, **kwargs)

    return astrosat_task_wrapper
