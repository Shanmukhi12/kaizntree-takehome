from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
import json
from rest_framework import status


# Create your tests here.

class ItemDashboardTest(APITestCase):
    def test_home_view(self):
        client = Client()

        # Make a GET request to the home view
        response = client.get(reverse('home'))

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'kaizntree/index.html')

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='riya', password='123')
        self.client.force_authenticate(user=self.user)

    def test_get_items(self):
        url = reverse('item_dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_items(self):
        url = reverse('item_dashboard')
        response = self.client.get(url, {'sku': 'BWAX'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_non_existing_items(self):
        url = reverse('item_dashboard')
        response = self.client.get(url, {'category': 'out_of_stock'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context['items']), 0)

    def test_invalid_query_params(self):
        url = reverse('item_dashboard')
        response = self.client.get(url, {'budget': 'value'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('items' in response.context)

    def test_signin_view(self):
        user = User.objects.create_user(username='paap', password='paap')
        data = {
            'username': 'paap',
            'pass1': 'paap',
        }
        response = self.client.post(reverse('signin'), data)
        self.assertEqual(response.status_code, 302)  # Check if user is redirected after signin
        self.assertIn('_auth_user_id', self.client.session)

    def test_signup_view(self):
        data = {
                'username': 'testuser',
                'fname': 'Test',
                'lname': 'User',
                'email': 'test@example.com',
                'pass1': 'testpass',
                'pass2': 'testpass',
            }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 302)  # Check if user is redirected after signup
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Check if user is created

    def test_unauthenticated_access(self):
        # Make a GET request to the item_dashboard endpoint without authenticating
        self.client.logout()

        # Make a GET request to the item_dashboard endpoint without authenticating
        url = reverse('item_dashboard')
        response = self.client.get(url)
        # Assert that the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)