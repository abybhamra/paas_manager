import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.test import TestCase, tag

from api.models import User, Resource


class TestUserModel(TestCase):

    def setUp(self):
        self.user_id = str(uuid.uuid1())
        self.user = User.objects.create(user_id=self.user_id,
                                        email='foo@bar.com',
                                        password='Qwerty@12',
                                        resources=10)

    def tearDown(self):
        self.user.delete()

    def test_a_valid_user_created_in_db_return_details_and_is_of_type_user(self):
        user_details = User.objects.get(email='foo@bar.com')
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(user_details.email, 'foo@bar.com')
        self.assertEqual(user_details.resources, '10')
        self.assertEqual(str(user_details), 'User ' + self.user_id + ' with email foo@bar.com has 10 resources left')

    @tag("WIP")
    def test_a_valid_repeat_user_raises_integrity_error(self):
        def create_repeat_object():
            try:
                User.objects.create(user_id=self.user.user_id,
                                    email='foobar@baz.com',
                                    password='Qwerty@12',
                                    resources=10)
            except:
                raise IntegrityError

        with self.assertRaises(IntegrityError):
            create_repeat_object()

    def test_to_get_user_with_email_that_is_not_of_type_user_raises_object_does_not_exist_error(self):
        def get_invalid_object():
            try:
                Resource.objects.get(email='something@not.there')
            except:
                raise ObjectDoesNotExist

        with self.assertRaises(ObjectDoesNotExist):
            get_invalid_object()


class TestResourceModel(TestCase):

    def setUp(self):
        self.guid = str(uuid.uuid4())
        self.user_id = str(uuid.uuid1())
        self.user = User.objects.create(user_id=self.user_id,
                                        email='foo@bar.com',
                                        password='Qwerty@12',
                                        resources=10)
        self.resource = Resource.objects.create(user=self.user, uuid=self.guid)

    def tearDown(self):
        self.user.delete()
        self.resource.delete()

    def test_a_valid_resource_created_in_db_return_details_and_is_of_type_resource(self):
        resource_details = Resource.objects.get(uuid=self.guid)
        self.assertTrue(isinstance(self.resource, Resource))
        self.assertEqual(resource_details.uuid, self.guid)
        self.assertEqual(resource_details.user.email, 'foo@bar.com')
        self.assertEqual(resource_details.user.resources, '10')
        self.assertEqual(str(resource_details), 'Resource id is ' + self.guid)

    def test_to_create_resource_with_an_invalid_object_relation_type_raises_value_error_error(self):
        def insert_invalid_object():
            try:
                Resource.objects.create(user='blah', uuid=self.guid)
            except:
                raise ValueError

        self.assertRaises(ValueError, insert_invalid_object)

    def test_to_get_resource_with_uuid_that_is_not_of_type_user_raises_object_does_not_exist_error(self):
        def get_invalid_object():
            try:
                Resource.objects.get(uuid=uuid.uuid4())
            except:
                raise ObjectDoesNotExist

        with self.assertRaises(ObjectDoesNotExist):
            get_invalid_object()
