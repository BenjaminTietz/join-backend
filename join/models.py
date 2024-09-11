from django.db import models
from django.db.models.fields import DateField
from datetime import date
from django.conf import settings
from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from phone_field import PhoneField

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    created_at = models.DateField(default=date.today) #for internal use
    #author = models.CharField(max_length=50) #for internal use
    #category = models.CharField(max_length=50)
    #priority = models.CharField(max_length=50)
    #status = models.CharField(max_length=50)
    #due_date = models.DateField()
    #sub_tasks = connect with subtask model
    #completed = models.BooleanField(default=False)
    #assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    checked = models.BooleanField(default=False)
    #created_at = models.DateField(default=date.today) #for internal use
    #author = models.CharField(max_length=50) #for internal use

    def __str__(self):
        return self.title
    
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = PhoneField(blank=True, help_text='Contact phone number')
    created_at = models.DateField(default=date.today) #for internal use

    def __str__(self):
        return ', '.join(f"{field.name}: {getattr(self, field.name)}" for field in self._meta.fields) 

class User(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        #user.set_password(validated_data['password'])  # safe method for hashing password
        user.save()
        return user

    class Meta:
        model = User
        # Tuple of serialized model fields 
        fields = ( "id", "username","email", "password", )