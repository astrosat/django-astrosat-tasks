from celery.exceptions import NotRegistered

from .celery import app as celery_app


def get_all_tasks():
    tasks = [
        task
        for task_name, task in sorted(celery_app.tasks.items())
        if not task_name.startswith("celery")
    ]
    return tasks


def get_task(task_name):
    try:
        task = celery_app.tasks[task_name]
        return task
    except NotRegistered:
        return None
