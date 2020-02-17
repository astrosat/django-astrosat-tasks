from rest_framework import serializers
from rest_framework.reverse import reverse_lazy

from django_celery_beat.models import PeriodicTask
from django_celery_results.models import TaskResult


#########################################
# a basic serializer for task schedules #
#########################################

class TaskScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = [
            "name",
            "enabled",
            "one_off",
            "last_run_at",
            "total_run_count",
            "task_args",
            "task_kwargs",
            "schedule",
        ]

    task_args = serializers.CharField(source="args")
    task_kwargs = serializers.CharField(source="kwargs")
    schedule = serializers.SerializerMethodField()

    def get_schedule(self, obj):
        schedule_type = "UNKNOWN"

        if obj.interval is not None:
            schedule_type = "interval"
        elif obj.crontab is not None:
            schedule_type = "crontab"
        elif obj.solar is not None:
            schedule_type = "solar"
        elif obj.clocked is not None:
            schedule_type = "clocked"

        return f"{schedule_type}: {obj.schedule}"


#######################################
# a basic serializer for task results #
#######################################

class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = [
            "date_created",
            "date_done",
            "status",
            "task_args",
            "task_kwargs",
            "result",
        ]



########################################
# the actual serializer used for tasks #
########################################

class TaskSerializer(serializers.BaseSerializer):
    """
    A read-only serializer for getting some useful information about a task:
    the upcoming schedules and the latest result.
    """

    def to_representation(self, instance):

        task_name = instance.name
        results_qs = TaskResult.objects.filter(task_name=task_name)
        schedules_qs = PeriodicTask.objects.filter(task=task_name)

        task_representation = {
            "name": task_name,
            "url": reverse_lazy(
                "tasks-detail", args=[task_name], request=self.context["request"],
            ),
            # "results": TaskResultSerializer(results_qs, many=True).data,
            "latest_result": TaskResultSerializer(results_qs.first()).data,
            "schedules": TaskScheduleSerializer(schedules_qs, many=True).data,
        }
        return task_representation
