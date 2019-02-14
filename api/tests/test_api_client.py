import uuid

from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient

from api.models import User, Resource
from api.serializers import UserSerializer




