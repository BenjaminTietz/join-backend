from django.db import models
from django.db.models.fields import DateField
from datetime import date
from django.conf import settings
from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import AbstractUser 
from phonenumber_field.modelfields import PhoneNumberField
from phone_field import PhoneField

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
        ('sales', 'Sales'),
        ('marketing', 'Marketing'),
        ('accounting', 'Accounting'),
        ('development', 'Development'),
        ('purchase', 'Purchase'),
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
    """
    Represents a contact in the system with fields for name, email, phone, initials, 
    color, and creation date.

    Attributes:
        id (int): The primary key for the contact.
        name (str): The name of the contact, limited to 50 characters.
        email (str): The contact's email address.
        phone (PhoneField): The contact's phone number, can be left blank.
        initials (str): The initials of the contact, can be left blank.
        color (str): The color associated with the contact (e.g., for UI display).
        created_at (date): The date the contact was created, defaults to today's date.
    """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = PhoneField(blank=True, help_text='Contact phone number')
    initials = models.CharField(blank=True,max_length=2)
    color = models.CharField(blank=True,max_length=7)
    created_at = models.DateField(default=date.today) #for internal use

    def __str__(self):
        """
        Returns the string representation of the Contact, which lists all fields and their values.
        """
        return ', '.join(f"{field.name}: {getattr(self, field.name)}" for field in self._meta.fields) 
    
class TaskContact(models.Model):
    """
    Represents the relationship between a Task and a Contact (many-to-many relationship).

    Attributes:
        task (Task): The related task.
        contact (Contact): The related contact.
    """
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

# CustomUser model with token-based authentication
class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser to use email instead of username 
    for authentication.

    Attributes:
        username (str): Optional username field, can be null or blank.
        email (str): The user's unique email address used for authentication.
    """
    
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']