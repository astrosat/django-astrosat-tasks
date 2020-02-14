from django.contrib import admin

from .models import ExampleThing


@admin.register(ExampleThing)
class ExampleThingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created",
        "modified",
    )
    list_filter = (
        "name",
        "created",
        "modified",
    )
    readonly_fields = (
        "created",
        "modified",
    )
