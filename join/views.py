from django.shortcuts import render
from rest_framework.authtoken.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets, status
from django_join_backend_app.serializers import UserSerializer, ContactSerializer, TaskSerializer, SubTaskSerializer, LoginSerializer
from .models import Contact, Task, SubTask, TaskContact
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SignupView(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []
    
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ContactView(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = Contact(
            name=serializer.validated_data['name'],
            email=serializer.validated_data['email'],
            phone=serializer.validated_data.get('phone', ''),
            initials=serializer.validated_data.get('initials', ''),
            color=serializer.validated_data.get('color', ''),
        )
        contact.save()
        return Response(ContactSerializer(contact).data)
    
    def retrieve(self, request, pk=None):
        try:
            contact = Contact.objects.get(id=pk)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found.'}, status=404)
        
        contact_serializer = ContactSerializer(contact)
        return Response(contact_serializer.data)
        
        
    def list(self, request):
        contacts = Contact.objects.all()  
        serializer = ContactSerializer(contacts, many=True)  
        return Response(serializer.data)  
    def update(self, request, pk=None):
        try:
            contact = Contact.objects.get(id=pk)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found.'}, status=404)

        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class TaskView(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
     
        task = serializer.save()
        
     
        assigned_contacts_data = request.data.get('assignedContacts', [])
        for contact_data in assigned_contacts_data:
            contact, created = Contact.objects.get_or_create(**contact_data)
            TaskContact.objects.get_or_create(task=task, contact=contact)

        return Response({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'category': task.category,
            'priority': task.priority,
            'status': task.status,
            'dueDate': task.dueDate,
        })
        
    def retrieve(self, request, pk=None):
        task = Task.objects.get(id=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
        
    def list(self, request):
        tasks = Task.objects.all()  
        serializer = TaskSerializer(tasks, many=True)  
        return Response(serializer.data)  
        
    def update(self, request, pk=None):
        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=404)

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def add_subtasks(self, request, pk=None):
        task = Task.objects.get(id=pk)
        subtask_data = request.data.get('subtasks', [])
        
        for subtask in subtask_data:
            SubTask.objects.create(
                task=task,
                title=subtask['title'],
                checked=subtask.get('checked', False)
            )
        
        return Response({'status': 'Subtasks added successfully'})
    
    def add_assignees(self, request, pk=None):
        status_message = []  
        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=404)

        assignee_data = request.data.get('assignedTo', [])

        for assignee in assignee_data:
            contact, created = Contact.objects.get_or_create(
                name=assignee['name'],
                email=assignee['email'],
                phone=assignee.get('phone', ''),
                initials=assignee.get('initials', ''),
                color=assignee.get('color', '')
            )
            
            
            TaskContact.objects.get_or_create(task=task, contact=contact)

            if created:
                status_message.append(f'Assignee {contact.name} created and added successfully.')
            else:
                status_message.append(f'Assignee {contact.name} already exists and was linked to the task.')

        return Response({'status': 'Assignees processed successfully', 'messages': status_message})
    
