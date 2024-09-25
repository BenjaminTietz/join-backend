from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Contact, Task

class ContactTests(APITestCase):
    def setUp(self):
        self.contact_data = {
            'name': 'Test Contact',
            'email': 'test@example.com',
            'phone': '1234567890'
        }

    def test_create_contact(self):
        response = self.client.post(reverse('contact'), self.contact_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().name, 'Test Contact')

    def test_list_contacts(self):
        self.client.post(reverse('contact'), self.contact_data)
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Contact')

    def test_retrieve_contact(self):
        contact = Contact.objects.create(**self.contact_data)
        response = self.client.get(reverse('contact', kwargs={'pk': contact.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], contact.name)

    def test_update_contact(self):
        contact = Contact.objects.create(**self.contact_data)
        updated_data = {'name': 'Updated Contact'}
        response = self.client.put(reverse('contact', kwargs={'pk': contact.pk}), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contact.refresh_from_db()
        self.assertEqual(contact.name, 'Updated Contact')

class TaskTests(APITestCase):
    def setUp(self):
        self.task_data = {
            'title': 'Test Task',
            'description': 'Task Description'
        }

    def test_create_task(self):
        response = self.client.post(reverse('task'), self.task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')

    def test_list_tasks(self):
        self.client.post(reverse('task'), self.task_data)
        response = self.client.get(reverse('task'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task')

    def test_retrieve_task(self):
        task = Task.objects.create(**self.task_data)
        response = self.client.get(reverse('task', kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], task.title)

    def test_update_task(self):
        task = Task.objects.create(**self.task_data)
        updated_data = {'title': 'Updated Task'}
        response = self.client.put(reverse('task', kwargs={'pk': task.pk}), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')
