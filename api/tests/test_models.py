import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.test import TestCase

from api.models import Resource, User


class TestUserModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             email='test@user.com',
                                             password='foobar')

    def test_a_valid_user(self):
        user_details = User.objects.get(username='test_user')
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(user_details.email, 'test@user.com')
        self.assertEqual(user_details.quota, None)

    def test_a_repeat_user_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username='test_user',
                                     email='test@user.com',
                                     password='foobar')

    def test_a_user_not_in_db_raises_object_does_not_exist_error(self):
        with self.assertRaises(ObjectDoesNotExist):
            random_user = 12312312312312313
            Resource.objects.get(user=random_user)


class TestResourceModel(TestCase):

    def setUp(self):
        self.guid = str(uuid.uuid4())
        self.user_id = str(uuid.uuid1())
        self.user = User.objects.create_user(username='test_user',
                                             email='test@user.com',
                                             password='foobar')
        self.resource = Resource.objects.create(user=self.user, uuid=self.guid)

    def test_a_valid_resource(self):
        resource_details = Resource.objects.get(uuid=self.guid)
        self.assertTrue(isinstance(self.resource, Resource))
        self.assertEqual(resource_details.uuid, self.guid)
        self.assertEqual(resource_details.user.email, 'test@user.com')
        self.assertEqual(str(resource_details), 'Resource id is ' + self.guid)

    def test_to_create_resource_with_an_invalid_user_object_relation_type_raises_value_error_error(self):
        with self.assertRaises(ValueError):
            Resource.objects.create(user='blah', uuid=self.guid)

    def test_to_get_resource_not_in_db_raises_object_does_not_exist_error(self):
        with self.assertRaises(ObjectDoesNotExist):
            Resource.objects.get(uuid=uuid.uuid4())
