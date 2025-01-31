from rest_framework.test import APITestCase, APIClient
from join_tasks.models import Task
from django.contrib.auth import get_user_model

class TaskViewTestCase(APITestCase):
    def setUp(self):
        User = get_user_model() 
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            category="frontend-angular",
            priority="medium",
            status="todo",
        )

    def test_task_retrieve(self):
        response = self.client.get(f"/task/{self.task.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.task.title)
