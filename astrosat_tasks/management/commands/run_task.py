import json
import warnings

from json.decoder import JSONDecodeError
from django.core.management.base import BaseCommand, CommandError

from astrosat_tasks.celery import app as celery_app
from astrosat_tasks.utils import get_task


class Command(BaseCommand):
    """
    Allows me to run a registered task as a one-off management command.
    Takes the fully-qualified task name and an argument list to pass to the task.
    If an argument contains commas, it is converted to a list.
    """

    help = "Runs a registered task."

    def add_arguments(self, parser):

        parser.add_argument(
            "--task-name",
            required=True,
            dest="task_name",
            help="The fully-qualified name of the task to run.",
        )

        parser.add_argument(
            "--task-args",
            default="[]",
            dest="task_args",
            help="A JSON list of arguments to pass to the task (ie: '[\"foo\", 23]')",
        )

        parser.add_argument(
            "--task-kwargs",
            default="{}",
            dest="task_kwargs",
            help="A JSON dictionary of arguments to pass to the task (ie: '{\"foo\": 23}')",
        )

        parser.add_argument(
            "--force",
            action="store_true",
            dest="force",
            help="Run the task immediately (synchronously) instead of submitting it to the broker (asynchronously)",
        )

        # keep track of the parser so I can have more informative error handling
        self.parser = parser

    def handle(self, *args, **options):

        task_name = options["task_name"]
        force = options.get("force")
        try:
            task_args = json.loads(options["task_args"])
            task_kwargs = json.loads(options["task_kwargs"])
        except JSONDecodeError:
            msg = "Error: invalid arguments.\n\n"
            raise CommandError(msg + self.parser.format_help())

        task = get_task(task_name)
        if task is None:
            msg = f"Error: {task_name} is not a registered task.  Be sure to use the fully-qualified name."
            raise CommandError(msg)

        try:
            with warnings.catch_warnings(record=True) as caught_warnings:
                warnings.simplefilter("always")

            task_result = task.apply_async(
                args=task_args, kwargs=task_kwargs, throw=True
            )  # throw=True causes errors to be thrown immediately
            if force:
                task_result.wait(timeout=None, propagate=True, interval=0.5)

            for w in caught_warnings:
                self.stderr.write(self.style.WARNING(w.message))

        except Exception as e:
            self.stderr.write(self.style.ERROR(e))
            raise CommandError(e)
