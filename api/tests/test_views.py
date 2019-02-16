import uuid
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from api.models import Resource, User
from api.models import UserManager


def create_user(email='', password=''):
    if email and password:
        get_user_model().objects.create(email=email, password=password)
        user = get_user_model().objects.get(email=email)
        return user


def create_resource(user):
    if user:
        guid = str(uuid.uuid4())
        res = Resource.objects.create(user=user, uuid=guid)
        return res


class TestUserViewSet(APITestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.user_mgr = UserManager()
        self.user = create_user(email='abhi@abhi.com', password='qwerty123')
        self.resource = create_resource(self.user)

    def test_normal_user_queries_users_get_permission_denied_403(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(reverse('user-list'), format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('permission_denied' in str(response.data))

    def test_admin_user_queries_users_gets_all_data_200(self):
        admin = User.objects.create(email='admin@abhi.com', password='qwerty123', is_admin=True)
        self.api_client.force_authenticate(user=admin)
        response = self.api_client.get(reverse('user-list'), format='json')

        self.assertIsInstance(response.data[0], OrderedDict)
        self.assertTrue(len(response.data[0]), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestResourceViewDetailsWithoutAuth(APITestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.user = create_user('abhi@abhi.com', 'qwerty')
        self.resource = create_resource(self.user)

    def test_update_or_delete_a_resource_without_credentials_gives_not_authenticated_403(self):
        response = self.api_client.put(reverse('resource-detail', args=[self.resource.uuid]), format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('not_authenticated' in str(response.data))


class TestResourceViewDetailsWithAuth(APITestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.email = 'aby@bhamra.com'
        self.password = 'qwerty123'
        self.user = create_user(self.email, self.password)
        self.resource = create_resource(self.user)
        self.api_client.force_authenticate(user=self.user)

    def tearDown(self):
        self.api_client.force_authenticate(user=None)

    def test_get_resources_returns_200(self):
        create_resource(create_user('aa@aa.com', 'qwerty'))
        create_resource(create_user('bb@bb.com', 'qwerty'))
        response = self.api_client.get(reverse('resource-list'), format='json')

        self.assertIsInstance(response.data[0], OrderedDict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_resource_details_returns_200(self):
        response = self.api_client.get(reverse('resource-detail', args=[self.resource.uuid]), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.resource.user.email)

    def test_create_a_resource_when_post_is_not_allowed_returns_method_not_allowed_405(self):
        response = self.api_client.post(reverse('resource-detail', args=[self.resource.uuid]), format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue('Method "POST" not allowed.' in str(response.data))

    def test_update_a_resource_based_on_email_id_with_valid_content_returns_200(self):
        new_uuid = "536d9992-a9b7-41d9-9868-8a66d9b5d90a"
        data = {'uuid': new_uuid, 'email': 'abhi@abhi.com'}
        response = self.api_client.put(reverse('resource-detail', args=[self.resource.uuid]),
                                       format='json', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_a_resource_returns_204(self):
        url = reverse('resource-detail', args=[self.resource.uuid])
        response = self.api_client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
