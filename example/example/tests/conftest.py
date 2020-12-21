import pytest
import factory
from factory.faker import (
    Faker as FactoryFaker,
)  # note I use FactoryBoy's wrapper of Faker

from django.contrib.auth import get_user_model

# from django.test import Client
# from rest_framework.test import APIClient

from astrosat_tasks.tests.factories import *


@pytest.fixture
def admin():
    UserModel = get_user_model()
    admin = UserModel.objects.create_superuser(
        "admin", "admin@test.com", "password"
    )
    return admin


@pytest.fixture
def user():
    UserModel = get_user_model()
    user = UserModel.objects.create_user("user", "user@test.com", "password")
    return user


# @pytest.fixture
# def client():
#     """
#     a client to use w/ the backend
#     """
#     client = Client(enforce_csrf_checks=False)
#     client.force_login(AnonymousUser())
#     return client

# @pytest.fixture
# def api_client(user):
#     """
#     a client to use w/ the API
#     w/ an already logged-in user
#     and a valid token & key
#     """
#     token, key = create_auth_token(user)
#     client = APIClient()
#     client.force_authenticate(user=user, token=token)
#     return (client, user, token, key)
