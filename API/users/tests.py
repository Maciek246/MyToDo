from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class UserAPITest(APITestCase):
    """
    api/users/login/
    api/users/logout/
    """

    @classmethod
    def setUpClass(cls):
        return super().setUpClass()

    def setUp(self):
        self._USER_DATA = {'username': 'TestUser1', 'password': 'password123'}

        self.user = User.objects.create_user(**self._USER_DATA)

        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)

        self.user_client = APIClient()

    def _login(self):
        self.user_client.login(**self._USER_DATA)

    def test_login_success(self):
        response = self.user_client.post('/api/users/login/', data=self._USER_DATA)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'token': self.token,
                                               'user': {'username': 'TestUser1'}})

    def test_login_fail(self):
        response = self.user_client.post('/api/users/login/')

        self.assertEqual(response.status_code, 400)

    def test_logout(self):
        self._login()
        response = self.user_client.post('/api/users/logout/')

        self.assertEqual(response.status_code, 200)
