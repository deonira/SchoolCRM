from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()
class AssistantAuthTests(APITestCase):

    def setUp(self):

        self.assistant = User.objects.create_user(
            username='assistant_test',
            password='testpassword123',
            is_assistant=True
        )
        self.login_url = '/api/auth/assistant-login/'
        self.dashboard_url = '/api/auth/assistant-dashboard/'
        self.token_url = '/api/auth/token/'
        self.token_refresh_url = '/api/auth/token/refresh/'

    def test_assistant_login_success(self):

        response = self.client.post(self.token_url, {
            'username': 'assistant_test',
            'password': 'testpassword123',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)




        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_assistant_login_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'assistant_test',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_dashboard_with_valid_token(self):
        response = self.client.post(self.token_url, {
            'username': 'assistant_test',
            'password': 'testpassword123',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        dashboard_response = self.client.get(self.dashboard_url)
        self.assertEqual(dashboard_response.status_code, status.HTTP_200_OK)
        self.assertEqual(dashboard_response.data['message'], 'Добро пожаловать, ассистент!')

    def test_access_dashboard_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        response = self.client.post(self.token_url, {
            'username': 'assistant_test',
            'password': 'testpassword123',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.data['refresh']

        refresh_response = self.client.post(self.token_refresh_url, {
            'refresh': refresh_token,
        })
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

    def test_dashboard_access_for_non_assistant(self):
        user = User.objects.create_user(username='regular_user', password='testpassword123')

        response = self.client.post(self.token_url, {
            'username': 'regular_user',
            'password': 'testpassword123',
        })
        access_token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        dashboard_response = self.client.get(self.dashboard_url)
        self.assertEqual(dashboard_response.status_code, status.HTTP_403_FORBIDDEN)