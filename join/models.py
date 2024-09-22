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
        return self.title
    
class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subTasks')
    title = models.CharField(max_length=50)
    checked = models.BooleanField(default=False)
    created_at = models.DateField(default=date.today) #for internal use
    #author = models.CharField(max_length=50) #for internal use

    def __str__(self):
        return self.title
    
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = PhoneField(blank=True, help_text='Contact phone number')
    initials = models.CharField(blank=True,max_length=2)
    color = models.CharField(blank=True,max_length=7)
    created_at = models.DateField(default=date.today) #for internal use

    def __str__(self):
        return ', '.join(f"{field.name}: {getattr(self, field.name)}" for field in self._meta.fields) 
class TaskContact(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

#CustomUser model mit Token
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']