from django.test import TestCase
from custom_auth.models import User
from join_contacts.models import Contact

class UserSignalTests(TestCase):
    def test_create_contact_for_user(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="TestPass123")
        self.assertIsNotNone(user.contact_id)
        self.assertEqual(user.contact_id.name, "testuser")

    def test_send_activation_email_signal(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="TestPass123", is_active=False)
