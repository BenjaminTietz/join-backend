from django.core.management.base import BaseCommand
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from join_tasks.models import Task, SubTask, TaskContact
from join_contacts.models import Contact
from datetime import date, timedelta
import random

def generate_demo_data(sender, user, **kwargs):
    TaskContact.objects.all().delete()
    SubTask.objects.all().delete()
    Task.objects.all().delete()

    
    demo_emails = [
        "alice.johnson@example.com", "bob.smith@example.com", "cathy.lee@example.com",
        "david.kim@example.com", "eva.thompson@example.com", "franklin.wright@example.com",
        "grace.park@example.com", "henry.scott@example.com", "irene.chen@example.com",
        "jack.tan@example.com",
    ]
    
    Contact.objects.filter(email__in=demo_emails).delete()
    
    demo_contacts = [
        {"name": "Alice Johnson", "email": "alice.johnson@example.com", "phone": "111-222-3333"},
        {"name": "Bob Smith", "email": "bob.smith@example.com", "phone": "222-333-4444"},
        {"name": "Cathy Lee", "email": "cathy.lee@example.com", "phone": "333-444-5555"},
        {"name": "David Kim", "email": "david.kim@example.com", "phone": "444-555-6666"},
        {"name": "Eva Thompson", "email": "eva.thompson@example.com", "phone": "555-666-7777"},
        {"name": "Franklin Wright", "email": "franklin.wright@example.com", "phone": "666-777-8888"},
        {"name": "Grace Park", "email": "grace.park@example.com", "phone": "777-888-9999"},
        {"name": "Henry Scott", "email": "henry.scott@example.com", "phone": "888-999-0000"},
        {"name": "Irene Chen", "email": "irene.chen@example.com", "phone": "999-000-1111"},
        {"name": "Jack Tan", "email": "jack.tan@example.com", "phone": "000-111-2222"},
    ]

    contacts = [Contact.objects.create(**contact_data) for contact_data in demo_contacts]

    CATEGORY_CHOICES = [
        'frontend-angular', 'backend-django', 'authentication', 'deployment', 'testing', 'project-management'
    ]
    PRIORITY_CHOICES = ['low', 'medium', 'urgent']
    STATUS_CHOICES = ['todo', 'inProgress', 'awaitFeedback', 'done']

    demo_tasks = [
        {"title": "Set up Angular Project Structure", "description": "Initialize Angular 18 project with required dependencies.", "category": "frontend-angular"},
        {"title": "Implement AuthGuard in Angular", "description": "Set up route guards to protect routes.", "category": "authentication"},
        {"title": "Build API Endpoints in Django", "description": "Develop API endpoints with Django REST framework.", "category": "backend-django"},
        {"title": "Implement AuthInterceptor", "description": "Manage authentication tokens using Angular interceptors.", "category": "authentication"},
        {"title": "Design User Interface for Kanban Board", "description": "Create a drag-and-drop interface using Angular.", "category": "frontend-angular"},
        {"title": "Setup Database Models in Django", "description": "Design database models for tasks and contacts.", "category": "backend-django"},
        {"title": "Set Up Docker for Deployment", "description": "Create Docker configurations for deployment.", "category": "deployment"},
        {"title": "Write Unit Tests for Angular Components", "description": "Implement unit tests for various Angular components.", "category": "testing"},
        {"title": "Configure Authentication API in Django", "description": "Implement authentication endpoints.", "category": "backend-django"},
        {"title": "Implement Drag and Drop in Angular", "description": "Use Angular CDK for a drag-and-drop feature.", "category": "frontend-angular"},
        {"title": "Set up CI/CD Pipeline", "description": "Integrate continuous integration and deployment pipeline.", "category": "deployment"},
        {"title": "Final Review and Client Meeting", "description": "Prepare for final project review with the client.", "category": "project-management"},
        {"title": "Integrate JWT Authentication", "description": "Configure JWT for secure communication.", "category": "authentication"},
        {"title": "Frontend Form Validations", "description": "Implement form validation for user inputs.", "category": "frontend-angular"},
        {"title": "User Profile Management", "description": "Build user profile management features.", "category": "frontend-angular"},
        {"title": "Automated Testing for API Endpoints", "description": "Write automated tests for backend APIs.", "category": "testing"},
        {"title": "Optimize Database Queries", "description": "Improve performance by optimizing queries.", "category": "backend-django"},
        {"title": "Code Review and Refactoring", "description": "Conduct code review and refactor as needed.", "category": "project-management"},
        {"title": "Setup Permissions and Access Control", "description": "Implement role-based access control.", "category": "backend-django"},
        {"title": "Document API with Swagger", "description": "Generate Swagger documentation for APIs.", "category": "backend-django"},
    ]

    tasks = []
    for task_data in demo_tasks:
        due_date = date.today() + timedelta(days=random.randint(1, 30))
        task = Task.objects.create(
            title=task_data["title"],
            description=task_data["description"],
            category=task_data["category"],
            priority=random.choice(PRIORITY_CHOICES),
            status=random.choice(STATUS_CHOICES),
            due_date=due_date
        )
        tasks.append(task)

        assigned_contacts = random.sample(contacts, random.randint(1, len(contacts) // 2))
        for contact in assigned_contacts:
            TaskContact.objects.create(task=task, contact=contact)

        for i in range(random.randint(3, 6)):
            SubTask.objects.create(
                task=task,
                title=f"{task.title} - SubTask {i + 1}",
                checked=random.choice([True, False]),
            )