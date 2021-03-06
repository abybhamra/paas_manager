import uuid

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.test import TestCase

from api.models import Resource, User


class TestUserManager(TestCase):
    def test_create_a_invalid_user_raises_value_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='',
                                     password='foobar')

    def test_create_a_valid_user(self):
        user = User.objects.create_user(email='test@user.com',
                                        password='foobar')
        user_details = User.objects.get(email='test@user.com')
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user_details.email, 'test@user.com')
        self.assertEqual(user_details.quota, None)

    def test_create_a_invalid_super_user_raises_value_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='test@user.com',
                                          password='foobar', is_admin=False)

    def test_create_a_valid_super_user(self):
        user = User.objects.create_superuser(email='test@user.com',
                                             password='foobar', is_admin=True)
        user_details = User.objects.get(email='test@user.com')
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user_details.email, 'test@user.com')
        self.assertEqual(user_details.quota, None)


class TestUserModel(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@user.com',
                                        password='foobar')

    def test_a_valid_user(self):
        user_details = User.objects.get(email='test@user.com')
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(user_details.email, 'test@user.com')
        self.assertEqual(user_details.quota, None)

    def test_a_repeat_user_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email='test@user.com',
                                     password='foobar')

    def test_a_user_not_in_db_raises_object_does_not_exist_error(self):
        with self.assertRaises(ObjectDoesNotExist):
            random_user = 12312312312312313
            Resource.objects.get(user=random_user)


class TestResourceModel(TestCase):

    def setUp(self):
        self.guid = str(uuid.uuid4())
        self.email = 'test@user.com'
        User.objects.create(email=self.email, password='foobar')
        self.user = User.objects.get(email=self.email)

    def test_a_valid_resource(self):
        resource = Resource.objects.create(user=self.user, uuid=self.guid)
        resource_details = Resource.objects.get(uuid=self.guid)
        self.assertTrue(isinstance(resource, Resource))
        self.assertTrue(self.guid in str(resource_details.uuid))
        self.assertEqual(resource_details.user.email, 'test@user.com')
        self.assertEqual(str(resource_details), 'Resource id ' + self.guid)

    def test_to_create_resource_with_an_invalid_user_object_relation_type_raises_attribute_error_error(self):
        with self.assertRaises(AttributeError):
            Resource.objects.create(user='blah', uuid=self.guid)

    def test_to_get_resource_not_in_db_raises_object_does_not_exist_error(self):
        with self.assertRaises(ObjectDoesNotExist):
            Resource.objects.get(uuid=uuid.uuid4())

    def test_should_raise_a_validation_error_when_users_number_of_resources_exceed_the_quota(self):
        User.objects.create(email='check@resources.com', password='foobar', quota=1)
        user = User.objects.get(email='check@resources.com')
        Resource.objects.create(user=user, uuid=uuid.uuid4())
        with self.assertRaises(ValidationError) as error:
            Resource.objects.create(user=user, uuid=uuid.uuid4())

        self.assertEqual(error.exception.message, "Resource limit exceeded!")
