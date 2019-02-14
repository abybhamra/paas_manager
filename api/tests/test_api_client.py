import uuid

from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient

from api.models import User, Resource
from api.serializers import UserSerializer


class TestAPI(APITestCase):

    @staticmethod
    def create_user(email='', password=''):
        if email and password:
            user_id = str(uuid.uuid1())
            user = User.objects.create(user_id=user_id, email=email, password=password, resources=10)
            return user

    @staticmethod
    def create_resource(user):
        if user:
            guid = str(uuid.uuid4())
            res = Resource.objects.create(user=user, uuid=guid)
            return res

    def setUp(self):
        self.api_client = APIClient()
        self.user_a = self.create_user("a@a.com", "qwerty")
        self.user_b = self.create_user("b@b.com", "qwerty")
        self.user_c = self.create_user("c@c.com", "qwerty")
        self.user_d = self.create_user("d@d.com", "qwerty")
        self.res_a = self.create_resource(self.user_a)
        self.res_b = self.create_resource(self.user_b)
        self.res_c = self.create_resource(self.user_c)
        self.res_d = self.create_resource(self.user_d)

    def tearDown(self):
        self.user_a.delete()
        self.user_b.delete()
        self.user_c.delete()
        self.user_d.delete()
        self.res_a.delete()
        self.res_b.delete()
        self.res_c.delete()
        self.res_d.delete()

    def test_get_all_users(self):
        response = self.api_client.get(reverse("users-all"))
        expected_output = User.objects.all()
        serialized = UserSerializer(expected_output, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

