from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from join_contacts.models import Contact
from django.contrib.auth import get_user_model

class ContactViewTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.contact = Contact.objects.create(
            name="John Doe",
            email="johndoe@example.com",
        )

        self.contact_data = {
            "name": "Jane Doe",
            "email": "janedoe@example.com",
            "phone": "+123456789",
        }


    def test_contact_creation(self):
        response = self.client.post("/contacts/", self.contact_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Jane Doe")

    def test_contact_retrieve(self):
        response = self.client.get(f"/contacts/{self.contact.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.contact.name)

    def test_contact_list(self):
        contacts_count = Contact.objects.count()
        response = self.client.get("/contacts/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), contacts_count)

    def test_contact_update(self):
        updated_data = {"name": "John Updated"}
        response = self.client.put(f"/contacts/{self.contact.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "John Updated")

    def test_contact_deletion(self):
        response = self.client.delete(f"/contacts/{self.contact.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Contact.objects.filter(id=self.contact.id).exists())
