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
from django.conf import settings

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
                'user': UserSerializer(user).data
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
    
    def delete(self, request, pk=None):
        """
        Handle DELETE request to delete a contact.

        Parameters:
        - pk: Primary key of the contact to delete.

        Returns:
        - Response: JSON response indicating success or failure.
        """
        try:
            contact = Contact.objects.get(id=pk)
            contact.delete()
            return Response({'status': 'Contact deleted successfully'})
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found.'}, status=404)
        
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
    
    def remove_subtasks(self, request, pk=None):
        """
        Handle DELETE request to remove subtasks from a task.

        Parameters:
        - pk: Primary key of the task.

        Returns:
        - Response: JSON response indicating success or failure.
        """
        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=404)

        subtask_data = request.data.get('subtasks', [])
        status_message = []

        for subtask in subtask_data:
            try:
                subtask_instance = SubTask.objects.get(task=task, title=subtask['title'])
                subtask_instance.delete()
                status_message.append(f'Subtask {subtask_instance.title} removed successfully.')
            except SubTask.DoesNotExist:
                status_message.append(f'Subtask {subtask["title"]} not found.')

        return Response({'status': 'Subtasks processed', 'messages': status_message})
    
    def update_subtask_status(self, request, task_pk=None, subtask_pk=None):
        """
        Handle PATCH request to update the 'checked' status of a subtask.

        Parameters:
        - task_pk: Primary key of the parent task.
        - subtask_pk: Primary key of the subtask to update.
        
        Returns:
        - Response: JSON response indicating success or failure.
        """
        try:
            task = Task.objects.get(id=task_pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=404)
        
        try:
            subtask = SubTask.objects.get(id=subtask_pk, task=task)
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found.'}, status=404)
        
        checked_status = request.data.get('checked')
        if checked_status is not None:
            subtask.checked = checked_status
            subtask.save()
            return Response({'status': 'Subtask updated successfully', 'checked': subtask.checked})
        
        return Response({'error': 'Invalid data provided.'}, status=400)
    def update_subtask(self, request, task_pk=None, subtask_pk=None):
        """
        Handle PATCH request to update a subtask's title and other fields.

        Parameters:
        - task_pk: Primary key of the parent task.
        - subtask_pk: Primary key of the subtask to update.

        Returns:
        - Response: JSON response indicating success or failure.
        """
        try:
            task = Task.objects.get(id=task_pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=404)
        
        try:
            subtask = SubTask.objects.get(id=subtask_pk, task=task)
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found.'}, status=404)

        new_title = request.data.get('title')
        
        if new_title is not None:
            subtask.title = new_title
        
        subtask.checked = request.data.get('checked', subtask.checked)

        subtask.save()
        
        return Response({
            'status': 'Subtask updated successfully',
            'subtask': SubTaskSerializer(subtask).data
        })
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
            try:
                contact = Contact.objects.get(
                    name=assignee['name'],
                    email=assignee['email']
                )
                
                TaskContact.objects.get_or_create(task=task, contact=contact)
                status_message.append(f'Assignee {contact.name} linked to the task successfully.')
            
            except Contact.DoesNotExist:
                status_message.append(f'Assignee {assignee["name"]} not found. No changes made.')

        return Response({'status': 'Assignees processed successfully', 'messages': status_message})
    
    def remove_assignees(self, request, pk=None):
        """
        Handle DELETE request to remove assignees from an existing task.

        Parameters:
        - pk: Primary key of the task.

        Returns:
        - Response: JSON response with status and processing messages.
        """
        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=404)

        assignee_data = request.data.get('assignedTo', [])
        status_message = []

        for assignee in assignee_data:
            try:
                contact = Contact.objects.get(
                    name=assignee['name'],
                    email=assignee['email'],
                )
                task_contact = TaskContact.objects.get(task=task, contact=contact)
                task_contact.delete()
                status_message.append(f'Assignee {contact.name} removed successfully.')
            except (Contact.DoesNotExist, TaskContact.DoesNotExist):
                status_message.append(f'Assignee {assignee["name"]} not found for this task.')

        return Response({'status': 'Assignees processed', 'messages': status_message})
    
class DocsView(viewsets.ViewSet):
    def get(self, request):
        """
        View to redirect the user to the Sphinx-generated documentation.

        This view handles requests by redirecting them to the static HTML 
        documentation generated by Sphinx, located at '/_build/html/index.html'.

        Args:
            request: The HTTP request object.

        Returns:
            A redirect response to the '/_build/html/index.html' page.
        """
        return redirect(f'{settings.STATIC_URL}index.html')   