from django.db import models
from django.utils.translation import gettext_lazy as _

from astrosat.mixins import SingletonMixin


class TaskSettings(SingletonMixin, models.Model):
    class Meta:
        verbose_name = "Task Settings"
        verbose_name_plural = "Task Settings"

    enable_celery = models.BooleanField(
        default=True, help_text=_("Enable the task management system.")
    )

    def __str__(self):
        return "Task Settings"
