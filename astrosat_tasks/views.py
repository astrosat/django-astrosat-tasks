from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from .conf import app_settings
from .serializers import TaskSerializer, TaskResultSerializer, TaskScheduleSerializer
from .utils import get_all_tasks, get_task


##############################################
# some "dummy" serializers to use w/ swagger #
##############################################

class _SwaggerTaskRequestSerializer(serializers.Serializer):
    task_args = serializers.JSONField()
    task_kwargs = serializers.JSONField()
    force = serializers.BooleanField(default=False)


class _SwaggerTaskResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.URLField()
    latest_result = TaskResultSerializer(many=False)
    schedules = TaskScheduleSerializer(many=True)


##################
# list ALL tasks #
##################

@swagger_auto_schema(
    method="get",
    responses={status.HTTP_200_OK: _SwaggerTaskResponseSerializer(many=True)},
)
@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def task_list_view(request):
    """
    Lists all tasks registered by this app w/ celery.
    """
    queryset = get_all_tasks()
    serializer = TaskSerializer(queryset, many=True, context={"request": request})
    return Response(serializer.data)


############################
# list and/or run ONE task #
############################

@swagger_auto_schema(
    method="get",
    responses={status.HTTP_200_OK: _SwaggerTaskResponseSerializer(many=False)},
)
@swagger_auto_schema(
    method="post",
    request_body=_SwaggerTaskRequestSerializer,
    responses={status.HTTP_200_OK: _SwaggerTaskResponseSerializer(many=False)},
)
@api_view(http_method_names=["GET", "POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def task_detail_view(request, task_name):
    """
    Lists and/or runs a task via celery.
    """
    task = get_task(task_name)
    if task is None:
        msg = f"Error: '{task_name}' is not a registered task.  Be sure to use the fully-qualified name."
        raise APIException(msg)

    if request.method == "POST":
        # a POST actually tries to run the task before serializing it
        if not app_settings.ASTROSAT_TASKS_ENABLE_CELERY:
            raise APIException("CELERY is currently disabled.")
        task_args = request.data.get("task_args", [])
        task_kwargs = request.data.get("task_kwargs", {})
        if not (isinstance(task_args, list) and isinstance(task_kwargs, dict)):
            raise APIException("Invalid args or kwargs")

        try:
            task_result = task.apply_async(
                args=task_args, kwargs=task_kwargs, throw=True
            )
            if request.data.get("force", False):
                task_result.wait(timeout=None, propagate=True, interval=0.5)
        except Exception as e:
            msg = f"Something went wrong: {e}."
            raise APIException(msg)

    serializer = TaskSerializer(task, context={"request": request})
    return Response(serializer.data)
