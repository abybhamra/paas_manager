import uuid

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from api.models import Resource
from api.serializers import UserSerializer


def create_user(username='', email='', password=''):
    if username and email and password:
        user = User.objects.create(username=username, email=email, password=password)
        return user


def create_resource(user):
    if user:
        guid = str(uuid.uuid4())
        res = Resource.objects.create(user=user, uuid=guid)
        return res


class TestResourceViewListMethod(APITestCase):

    def setUp(self):
        self.api_client = APIClient()

    def test_get_resource_when_no_resources_in_db(self):
        response = self.api_client.get(reverse('resources-list'), format='json')

        expected_output = Resource.objects.all()
        serialized = UserSerializer(expected_output, many=True)

        self.assertEqual(response.data, [])
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_resources_when_resources_are_added_in_db(self):
        create_resource(create_user('aa_aa', 'aa@aa.com', 'qwerty'))
        create_resource(create_user('bb_bb', 'bb@bb.com', 'qwerty'))
        create_resource(create_user('cc_cc', 'cc@cc.com', 'qwerty'))
        create_resource(create_user('dd_dd', 'dd@dd.com', 'qwerty'))
        response = self.api_client.get(reverse('resources-list'), format='json')

        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestResourceViewDetails(APITestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.resource = create_resource(create_user('abhi', 'abhi@abhi.com', 'qwerty'))

    def test_get_resource_details(self):
        response = self.api_client.get(reverse('resource-details', args=[self.resource.user_id]), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.resource.user.email)

    def test_update_or_delete_a_resource_without_credentials_gives_not_authenticated(self):
        response = self.api_client.put(reverse('resource-details', args=[self.resource.user_id]), format='json')

        self.assertTrue('not_authenticated' in str(response.data))


class TestResourceViewDetailsWithAuth(APITestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.username = 'aby@bhamra.com'
        self.password = 'qwerty123'
        self.user = create_user(self.username, 'abhi@abhi.com', self.password)
        self.resource = create_resource(self.user)
        self.api_client.force_authenticate(user=self.user)

    def tearDown(self):
        self.api_client.force_authenticate(user=None)

    def test_create_a_resource_when_post_is_not_allowed_gives_405_method_not_allowed(self):
        response = self.api_client.post(reverse('resource-details', args=[self.resource.user_id]), format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue('Method "POST" not allowed.' in str(response.data))

    def test_update_a_resource_based_on_email_id_with_valid_content(self):
        new_uuid = "536d9992-a9b7-41d9-9868-8a66d9b5d90a"
        data = {'uuid': new_uuid, 'email': 'abhi@abhi.com'}
        response = self.api_client.put(reverse('resource-details', args=[self.resource.user_id]),
                                       format='json', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_a_resource(self):
        url = reverse('resource-details', args=[self.resource.user_id])
        response = self.api_client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
