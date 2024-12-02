from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient
from django.core.management import call_command
from django.core.management.base import BaseCommand
from join.management.commands.generate_demo_data import generate_demo_data
from io import StringIO
class DocsViewTestCase(TestCase):
    def test_docs_redirect(self):
        response = self.client.get(reverse('docs_view')) 
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(response.url, f"{settings.STATIC_URL}index.html") 

class GenerateDemoDataViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_generate_demo_data(self):
        response = self.client.post(reverse('generate-demo-data'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Demo data generated successfully."}) 


class GetCsrfTokenViewTestCase(TestCase):
    def test_get_csrf_token(self):
        response = self.client.get(reverse('get-csrf-token'))  
        self.assertEqual(response.status_code, 200)  
        self.assertIn('csrfToken', response.json())  





