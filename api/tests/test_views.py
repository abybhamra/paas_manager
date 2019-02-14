import uuid

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from api.models import User, Resource
from api.serializers import UserSerializer


def create_user(email='', password=''):
    if email and password:
        user_id = str(uuid.uuid1())
        user = User.objects.create(user_id=user_id, email=email, password=password, resources=10)
        return user


def create_resource(user):
    if user:
        guid = str(uuid.uuid4())
        res = Resource.objects.create(user=user, uuid=guid)
        return res


class TestUserViewListMethod(APITestCase):

    def setUp(self):
        self.api_client = APIClient()

    def test_get_users_when_no_users_in_db(self):
        response = self.api_client.get(reverse('users-list'), format='json')

        expected_output = User.objects.all()
        serialized = UserSerializer(expected_output, many=True)

        self.assertEqual(response.data, [])
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users_when_users_are_added_in_db(self):
        create_user('aa@aa.com', 'qwerty')
        create_user('bb@bb.com', 'qwerty')
        create_user('cc@cc.com', 'qwerty')
        create_user('dd@dd.com', 'qwerty')
        response = self.api_client.get(reverse('users-list'), format='json')

        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserViewDetails(APITestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.user1 = create_user('abhi@abhi.com', 'qwerty')
        self.user2 = create_user('tobedeleted@tobedeleted.com', 'qwerty')

    def test_get_user(self):
        response = self.api_client.get(reverse('user-details', args=[self.user1.user_id]), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"user_id": self.user1.user_id, "email": self.user1.email})

    def test_update_user_should_return_bad_request_when_invalid_data_is_passed(self):
        response = self.api_client.put(reverse('user-details', args=[self.user1.user_id]), format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["email"][0].code, "required")

    def test_update_a_user_based_on_email_id_with_valid_content(self):
        data = {'user_id': self.user1.user_id, 'email': 'new@email.com'}
        response = self.api_client.put(reverse('user-details', args=[self.user1.user_id]),
                                       format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_a_users_based_on_email_id(self):
        url = reverse('user-details', args=[self.user1.user_id])
        response = self.api_client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
