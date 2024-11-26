from django.db import models
from django.db.models.fields import DateField
from datetime import date
from django.conf import settings
from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import AbstractUser 
from phonenumber_field.modelfields import PhoneNumberField
from phone_field import PhoneField
import random
from join_contacts.models import Contact

# Create your models here.
class Task(models.Model):
    """
    Represents a task in the system with fields for title, description, category, 
    priority, status, and due date.

    Attributes:
        id (int): The primary key for the task.
        title (str): The title of the task, limited to 50 characters.
        description (str): An optional detailed description of the task, limited to 500 characters.
        created_at (date): The date the task was created, defaults to today's date.
        created_by (str): The string identifier of the user who created the task.
        category (str): The category the task falls under, chosen from predefined categories.
        priority (str): The priority level of the task, chosen from predefined levels.
        status (str): The current status of the task, chosen from predefined statuses.
        due_date (date): The deadline by which the task should be completed, defaults to today's date.
    """
    
    CATEGORY_CHOICES = [
        ('frontend-angular', 'Frontend - Angular'),
        ('backend-django', 'Backend - Django'),
        ('authentication', 'Authentication'),
        ('deployment', 'Deployment'),
        ('testing', 'Testing'),
        ('project-management', 'Project Management'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('urgent', 'URGENT'),
    ]
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('inProgress', 'In Progress'),
        ('awaitFeedback', 'Await Feedback'),
        ('done', 'Done'),
    ]
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True, null=True)  
    created_at = models.DateField(default=date.today)
    created_by = models.CharField(max_length=255, default="system")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50, default='frontend-angular')
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=50, default='medium')
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='todo')
    due_date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.title} ({self.status})"
    
class SubTask(models.Model):
    """
    Represents a subtask that is associated with a specific task.

    Attributes:
        task (Task): The parent task to which the subtask belongs.
        title (str): The title of the subtask, limited to 50 characters.
        checked (bool): A boolean flag indicating whether the subtask is completed or not.
        created_at (date): The date the subtask was created, defaults to today's date.
    """
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subTasks')
    title = models.CharField(max_length=50)
    checked = models.BooleanField(default=False)
    created_at = models.DateField(default=date.today) #for internal use
    #author = models.CharField(max_length=50) #for internal use

    def __str__(self):
        """
        Returns the string representation of the SubTask, which is its title.
        """
        return self.title
    
    
class TaskContact(models.Model):
    """
    Represents the relationship between a Task and a Contact (many-to-many relationship).

    Attributes:
        task (Task): The related task.
        contact (Contact): The related contact.
    """
    
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    contact = models.ForeignKey('join_contacts.Contact', on_delete=models.SET_NULL, null=True)