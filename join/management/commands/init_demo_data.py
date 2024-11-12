from django.core.management.base import BaseCommand
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from join.models import Task, SubTask, Contact, TaskContact
from datetime import date, timedelta
import random

def generate_demo_data(sender, user, **kwargs):
    TaskContact.objects.all().delete()
    SubTask.objects.all().delete()
    Task.objects.all().delete()
    Contact.objects.all().delete()

    demo_contacts = [
        {"name": "Luca Bianchi", "email": "luca.bianchi@example.com", "phone": "123-456-7890"},
        {"name": "Sofia Schmidt", "email": "sofia.schmidt@example.com", "phone": "987-654-3210"},
        {"name": "Marta Kowalski", "email": "marta.kowalski@example.com", "phone": "555-555-5555"},
        {"name": "Ivan Novak", "email": "ivan.novak@example.com", "phone": "444-444-4444"},
        {"name": "Emma Dubois", "email": "emma.dubois@example.com", "phone": "333-333-3333"},
        {"name": "Noah Jensen", "email": "noah.jensen@example.com", "phone": "222-222-2222"},
        {"name": "Lucas Muller", "email": "lucas.muller@example.com", "phone": "111-111-1111"},
        {"name": "Elena Rossi", "email": "elena.rossi@example.com", "phone": "999-999-9999"},
        {"name": "Johan Svensson", "email": "johan.svensson@example.com", "phone": "888-888-8888"},
        {"name": "Ana Garcia", "email": "ana.garcia@example.com", "phone": "777-777-7777"},
    ]

    contacts = []
    for contact_data in demo_contacts:
        contact = Contact.objects.create(
            name=contact_data["name"],
            email=contact_data["email"],
            phone=contact_data["phone"],
        )
        contacts.append(contact)

    CATEGORY_CHOICES = ['development', 'project-management', 'deployment', 'testing', 'client-communication']
    PRIORITY_CHOICES = ['low', 'medium', 'urgent']
    STATUS_CHOICES = ['todo', 'inProgress', 'awaitFeedback', 'done']

    demo_tasks = [
        {"title": "Set Up Development Environment", "description": "Prepare all necessary tools and environments for the project.", "category": "development", "priority": "urgent", "status": "todo"},
        {"title": "Backend API Design", "description": "Design the REST API endpoints for the application.", "category": "development", "priority": "medium", "status": "inProgress"},
        {"title": "Frontend Framework Selection", "description": "Choose the most suitable frontend framework for the project.", "category": "project-management", "priority": "medium", "status": "awaitFeedback"},
        {"title": "Client Requirement Meeting", "description": "Discuss detailed requirements with the client.", "category": "client-communication", "priority": "urgent", "status": "done"},
        {"title": "Deployment Strategy Planning", "description": "Plan the deployment strategy, including CI/CD pipeline setup.", "category": "deployment", "priority": "medium", "status": "todo"},
        {"title": "Testing Suite Implementation", "description": "Implement a testing suite for automated unit and integration tests.", "category": "testing", "priority": "low", "status": "inProgress"},
        {"title": "Database Schema Design", "description": "Design the schema for the project database.", "category": "development", "priority": "urgent", "status": "todo"},
        {"title": "User Authentication Module", "description": "Develop the user authentication and authorization module.", "category": "development", "priority": "urgent", "status": "inProgress"},
        {"title": "Deployment to Staging Server", "description": "Deploy the application to the staging server for final review.", "category": "deployment", "priority": "medium", "status": "awaitFeedback"},
        {"title": "Final Client Review", "description": "Conduct the final review meeting with the client before the production release.", "category": "client-communication", "priority": "urgent", "status": "done"},
    ]

    tasks = []
    for task_data in demo_tasks:
        due_date = date.today() + timedelta(days=random.randint(1, 30))
        task = Task.objects.create(
            title=task_data["title"],
            description=task_data["description"],
            category=task_data["category"],
            priority=task_data["priority"],
            status=task_data["status"],
            dueDate=due_date
        )
        tasks.append(task)

        assigned_contacts = random.sample(contacts, random.randint(1, len(contacts)))
        for contact in assigned_contacts:
            TaskContact.objects.create(task=task, contact=contact)

        for i in range(random.randint(2, 6)):
            SubTask.objects.create(
                task=task,
                title=f"SubTask {i + 1} for {task.title}",
                checked=random.choice([True, False]),
            )


class Command(BaseCommand):
    help = 'Generate demo data for tasks, contacts, and subtasks'

    def handle(self, *args, **kwargs):
        generate_demo_data(sender=self.__class__, user=None)
        self.stdout.write(self.style.SUCCESS('Demo data generation completed successfully.'))