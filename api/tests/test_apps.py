import unittest

from api.apps import ApiConfig


class TestApp(unittest.TestCase):
    def test_app_returns_app_name(self):
        self.assertEqual(ApiConfig.name, 'api')
