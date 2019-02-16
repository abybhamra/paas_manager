from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from api.models import User
from api.permissions import IsAdminUser


class TestIsAdminUser(APITestCase):

    def setUp(self):
        self.is_admin = IsAdminUser()
        self.api_client = APIClient()
        self.user = User.objects.create_user(email='normal@user.com',
                                             password='foobar')
        self.admin = User.objects.create_superuser(email='admin@user.com',
                                                   password='foobar123', is_admin=True)

    def test_admin_user_returns_true(self):
        self.api_client.force_authenticate(user=self.admin)
        response = self.api_client.get(reverse('user-list'), format='json')
        request = response.wsgi_request

        self.assertTrue(self.is_admin.has_permission(request))
        self.api_client.logout()

    def test_normal_user_returns_false(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(reverse('user-list'), format='json')
        request = response.wsgi_request

        self.assertFalse(self.is_admin.has_permission(request))
