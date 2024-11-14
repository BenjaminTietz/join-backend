from django.shortcuts import redirect, render
from django.conf import settings
from django.core.management.base import BaseCommand
from join.management.commands.init_demo_data import generate_demo_data
from django.utils.decorators import method_decorator
from join_contacts.models import Contact
from join_contacts.serializers import ContactSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt

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