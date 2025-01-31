from django.test import TestCase
from join_tasks.models import Task

class TaskModelTestCase(TestCase):
    def test_task_creation(self):
        task = Task.objects.create(title="Test Task", status="todo")
        self.assertEqual(task.title, "Test Task")
