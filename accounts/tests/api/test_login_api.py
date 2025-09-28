from rest_framework import status
from rest_framework.authtoken.models import Token

from accounts.factories.user import UserFactory
from common.tests.isolated_cache_test_case import APITestCase


class UserAuthTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory()

    def test_user_login_default(self):
        response = self.client.post(
            '/api/accounts/login/', {
                'username': self.user.username,
                'password': self.user.raw_password,
            },
        )

        self.assert_login_success(response)

    def assertResponseStatus(self, response, status_code):
        self.assertEqual(response.status_code, status_code, response.content)

    def assert_login_success(self, response):
        self.assertResponseStatus(response, status.HTTP_200_OK)
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['token'], token.key)
        self.assertEqual(response.data['user']['name'], self.user.name)
