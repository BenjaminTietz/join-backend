from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.middleware.csrf import get_token
from rest_framework.authtoken.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets, status
from django_join_backend_app.serializers import TaskSerializer, SubTaskSerializer
from join_contacts.serializers import ContactSerializer
from custom_auth.serializers import UserSerializer
from join_tasks.models import Task, SubTask, TaskContact
from join_contacts.models import Contact
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from django.conf import settings
from django.core.management.base import BaseCommand
from join.management.commands.init_demo_data import generate_demo_data
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


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
    
    def delete(self, request, pk=None):
        """
        Handle DELETE request to remove a task.

        Parameters:
        - pk: Primary key of the task to delete.

        Returns:
        - Response: JSON response indicating success or failure.
        """
        try:
            task = Task.objects.get(id=pk)
            task.delete()
            return Response({'status': 'Task deleted successfully.'})
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=404)
        
    
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
    
    def remove_subtasks(self, request, pk=None, subtask_id=None):
        """
        Handle DELETE request to remove a specific subtask from a task.

        Parameters:
        - pk: Primary key of the task.
        - subtask_id: Primary key of the subtask to remove.

        Returns:
        - Response: JSON response indicating success or failure.
        """
        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=404)

        try:
            subtask_instance = SubTask.objects.get(id=subtask_id, task=task)
            subtask_instance.delete()
            return Response({'status': 'Subtask removed successfully.'})
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found.'}, status=404)
    

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
    
@method_decorator(csrf_exempt, name='dispatch')
class GenerateDemoDataView(View):
    def post(self, request, *args, **kwargs):
        generate_demo_data(sender=self.__class__, user=None)
        return JsonResponse({"message": "Demo data generated successfully."}, status=200)

class GetCsrfTokenView(View):
    def get(self, request, *args, **kwargs):
        token = get_token(request)
        return JsonResponse({'csrfToken': token}, status=200)

class Command(BaseCommand):
    help = 'Generate demo data for tasks, contacts, and subtasks'

    def handle(self, *args, **kwargs):
        generate_demo_data(sender=self.__class__, user=None)
        self.stdout.write(self.style.SUCCESS('Demo data generation completed successfully.'))