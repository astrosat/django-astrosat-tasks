from django.urls import include, path, re_path

from rest_framework.routers import SimpleRouter

from .conf import app_settings


##############
# API routes #
##############

api_router = SimpleRouter()
api_urlpatterns = [
    path("", include(api_router.urls)),
]


#################
# normal routes #
#################

urlpatterns = []
