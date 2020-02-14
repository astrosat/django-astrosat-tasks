from django.contrib import admin

from astrosat_tasks.models import TaskSettings


@admin.register(TaskSettings)
class TaskSettingsAdmin(admin.ModelAdmin):
    pass
