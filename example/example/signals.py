from django.dispatch import receiver

from django.db.models.signals import post_save, pre_save
from example.models import ExampleThing


@receiver(post_save, sender=ExampleThing)
def example_thing_post_save_handler(sender, *args, **kwargs):
    print("post_save ExampleThing")

@receiver(pre_save, sender=ExampleThing)
def example_thing_pre_save_handler(sender, *args, **kwargs):
    print("pre_save ExampleThing")
