from celery import shared_task
from celery.contrib.abortable import AbortableTask

from astrosat_tasks.decorators import conditional_task
from .models import ExampleThing


@shared_task
def add_some_numbers(*args, verbose=False):
    if verbose:
        print(f"going to add these numbers: {args}")
    return sum(args)


@shared_task
@conditional_task
def create_some_things(n, verbose=False):
    if verbose:
        print(f"going to create {n} things.")
    for _ in range(n):
        thing = ExampleThing(name=f"thing_{ExampleThing.objects.count()}")
        thing.save()


@shared_task
@conditional_task
def fail_at_some_task(verbose=False):
    if verbose:
        print("about to raise an error")
    raise RuntimeError()
