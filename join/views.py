from django.shortcuts import render
from rest_framework.authtoken.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets, status
from django_join_backend_app.serializers import UserSerializer, ContactSerializer, TaskSerializer, SubTaskSerializer, LoginSerializer
from .models import Contact, Task, SubTask, TaskContact
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect

class LoginView(APIView):
    """
    API view for user login.

    This view handles user authentication by validating login credentials
    and returning a token if authentication is successful.
    """
    authentication_classes = []
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST request for user login.

        Parameters:
        - request: HTTP request containing login data.

        Returns:
        - Response: JSON response with token on success or error messages on failure.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SignupView(viewsets.ViewSet):
    """
    API view for user registration (signup).

    This view handles the creation of new user accounts.
    """
    authentication_classes = []
    permission_classes = []
    
    def create(self, request):
        """
        Handle POST request for user registration.

        Parameters:
        - request: HTTP request containing user signup data.

        Returns:
        - Response: JSON response with user data on success or error messages on failure.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ContactView(viewsets.ViewSet):
    """
    API view for managing contacts.

    This view allows creating, retrieving, listing, and updating contact details.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        """
        Handle POST request to create a new contact.

        Parameters:
        - request: HTTP request containing contact data.

        Returns:
        - Response: JSON response with contact data on success.
        """
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
        """
        Handle GET request to retrieve contact details by ID.

        Parameters:
        - pk: Primary key of the contact to retrieve.

        Returns:
        - Response: JSON response with contact data on success or error message on failure.
        """
        try:
            contact = Contact.objects.get(id=pk)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found.'}, status=404)
        
        contact_serializer = ContactSerializer(contact)
        return Response(contact_serializer.data)
        
        
    def list(self, request):
        """
        Handle GET request to list all contacts.

        Returns:
        - Response: JSON response containing a list of all contacts.
        """
        contacts = Contact.objects.all()  
        serializer = ContactSerializer(contacts, many=True)  
        return Response(serializer.data)  
    def update(self, request, pk=None):
        """
        Handle PUT/PATCH request to update a contact's information.

        Parameters:
        - pk: Primary key of the contact to update.

        Returns:
        - Response: JSON response with updated contact data on success or error message on failure.
        """
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
    """
    API view for managing tasks.

    This view allows creating, retrieving, listing, updating tasks, and adding subtasks or assignees.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        """
        Handle POST request to create a new task.

        Parameters:
        - request: HTTP request containing task data.

        Returns:
        - Response: JSON response with task details on success.
        """
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
        """
        Handle GET request to retrieve a task by ID.

        Parameters:
        - pk: Primary key of the task to retrieve.

        Returns:
        - Response: JSON response with task details on success.
        """
        task = Task.objects.get(id=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
        
    def list(self, request):
        """
        Handle GET request to list all tasks.

        Returns:
        - Response: JSON response containing a list of all tasks.
        """
        tasks = Task.objects.all()  
        serializer = TaskSerializer(tasks, many=True)  
        return Response(serializer.data)  
        
    def update(self, request, pk=None):
        """
        Handle PUT/PATCH request to update a task.

        Parameters:
        - pk: Primary key of the task to update.

        Returns:
        - Response: JSON response with updated task data on success or error message on failure.
        """
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
        """
        Handle POST request to add subtasks to an existing task.

        Parameters:
        - pk: Primary key of the task to add subtasks to.

        Returns:
        - Response: JSON response indicating the status of the operation.
        """
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
        """
        Handle POST request to add assignees to an existing task.

        Parameters:
        - pk: Primary key of the task to add assignees to.

        Returns:
        - Response: JSON response with status and processing messages.
        """
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
    
def docs_view(request):
    """
    View to redirect the user to the Sphinx-generated documentation.

    This view handles requests by redirecting them to the static HTML 
    documentation generated by Sphinx, located at '/static/index.html'.

    Args:
        request: The HTTP request object.

    Returns:
        A redirect response to the '/static/index.html' page.
    """
    return redirect('/static/index.html')