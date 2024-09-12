from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets, status
from django_join_backend_app.serializers import UserSerializer, ContactSerializer, TaskSerializer
from .models import Contact, Task

# Create your views here.
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
class SignupView(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ContactView(viewsets.ViewSet):
    def create(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = Contact(
            name=serializer.validated_data['name'],
            email=serializer.validated_data['email'],
            phone=serializer.validated_data['phone']
        )
        contact.save()
        return Response({
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone
        })
        
class TaskView(viewsets.ViewSet):
    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = Task(
            title=serializer.validated_data['title'],
            description=serializer.validated_data['description'],
            category=serializer.validated_data['category'],
            priority=serializer.validated_data['priority'],
            status=serializer.validated_data['status'],
            due_date=serializer.validated_data['due_date']
        )
        task.save()
        return Response({
            'title': task.title,
            'description': task.description,
            'category': task.category,
            'priority': task.priority,
            'status': task.status,
            'due_date': task.due_date
        })