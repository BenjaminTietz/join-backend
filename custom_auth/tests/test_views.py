from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from custom_auth.models import User
from django.urls import reverse
import random
import string

class AuthViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')  
        self.login_url = reverse('login')    
        self.activation_url = reverse('activate_user', kwargs={'uidb64': 'fake_uid', 'token': 'fake_token'})

        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        self.user_data = {
            "username": f"testuser{random_string}",
            "email": f"testuser{random_string}@example.com",
            "password": "TestPass123",
            "phone": "1234567890"
        }
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password'],
            phone=self.user_data['phone'],
            is_active=True
        )

    def test_valid_login(self):
        response = self.client.post(self.login_url, {"email": self.user.email, "password": "TestPass123"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_invalid_login(self):
        response = self.client.post(self.login_url, {"email": self.user.email, "password": "WrongPass"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup(self):
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        data = {
            'username': f'testuser{random_string}',
            'email': f'testuser{random_string}@example.com',
            'password': 'testpassword123',
            'phone': '123-456-7890',
        }
        response = self.client.post('/auth/signup/', data, format='json')
        print(response.data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])

    def test_duplicate_signup(self):
        response = self.client.post(self.signup_url, self.user_data, format="json")
        response = self.client.post(self.signup_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activation_invalid_link(self):
        response = self.client.get(self.activation_url)
        self.assertEqual(response.status_code, 400)

