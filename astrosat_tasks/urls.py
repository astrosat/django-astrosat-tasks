from django.urls import include, path, re_path

from rest_framework.routers import SimpleRouter

from .views import task_list_view, task_detail_view

##############
# API routes #
##############

api_router = SimpleRouter()
api_urlpatterns = [
    path("", include(api_router.urls)),
    path("tasks/", task_list_view, name="tasks-list"),
    path("tasks/<str:task_name>/", task_detail_view, name="tasks-detail"),
]

#################
# normal routes #
#################

urlpatterns = []
