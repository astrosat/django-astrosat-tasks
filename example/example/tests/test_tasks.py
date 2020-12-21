# from django.urls import resolve, reverse

import pytest

from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestTaskSchedules:
    def test_foobar(self):
        assert True
