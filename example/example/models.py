from django.db import models
from django.utils.translation import ugettext_lazy as _


class ExampleThing(models.Model):
    """
    A silly model, just for testing.
    """

    name = models.CharField(max_length=128, blank=False, null=False)
    created = models.DateTimeField(
        auto_now_add=True, help_text=_("When the thing was first created.")
    )
    modified = models.DateTimeField(
        auto_now=True, help_text=_("When the thing was last modified.")
    )

    def __str__(self):
        return self.name
