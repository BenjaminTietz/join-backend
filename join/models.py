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

# Create your models here.
class Task(models.Model):
    """
    Represents a task in the system with fields for title, description, category, 
    priority, status, and due date.

    Attributes:
        id (int): The primary key for the task.
        title (str): The title of the task, limited to 50 characters.
        description (str): A detailed description of the task, limited to 500 characters.
        created_at (date): The date the task was created, defaults to today's date.
        category (str): The category the task falls under, chosen from predefined categories.
        priority (str): The priority level of the task, chosen from predefined levels.
        status (str): The current status of the task, chosen from predefined statuses.
        dueDate (date): The deadline by which the task should be completed, defaults to today's date.
    """
    
    CATEGORY_CHOICES = [
        ('testing', 'Testing'),
        ('client-communication', 'Client Communication'),
        ('project-management', 'Project Management'),
        ('development', 'Development'),
        ('deployment', 'Deployment'),
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
    description = models.TextField(max_length=500)
    created_at = models.DateField(default=date.today) #for internal use
    #author = models.CharField(max_length=50) #for internal use
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50, default='development')
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=50, default='medium')
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='todo')
    dueDate = models.DateField(default=date.today)

    def __str__(self):
        """
        Returns the string representation of the Task, which is its title.
        """
        return self.title
    
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
    
class Contact(models.Model):
    COLOR_CHOICES = [
        "#6E52FF",  # blue
        "#462F8A",  # dark blue
        "#FC71FF",  # pink
        "#9327FF",  # purple
        "#FF7A00",  # orange
        "#1FD7C1",  # light green
        "#FF4646",  # red
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = PhoneField(blank=True, help_text='Contact phone number')
    initials = models.CharField(max_length=2, blank=True)
    color = models.CharField(max_length=7, blank=True, default='')
    created_at = models.DateField(default=date.today)

    def save(self, *args, **kwargs):
        if not self.initials and self.name:
            self.initials = ''.join([n[0] for n in self.name.split()[:2]]).upper()
        if not self.color:
            self.color = random.choice(self.COLOR_CHOICES)
        super().save(*args, **kwargs)
    
class TaskContact(models.Model):
    """
    Represents the relationship between a Task and a Contact (many-to-many relationship).

    Attributes:
        task (Task): The related task.
        contact (Contact): The related contact.
    """
    
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)