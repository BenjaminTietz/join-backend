from rest_framework import serializers
from join_tasks.models import Task, SubTask, TaskContact
from join_contacts.serializers import ContactSerializer
from join_tasks.serializers import TaskSerializer, SubTaskSerializer
from custom_auth.models import User
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate

        
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login. Validates the provided email and password,
    and authenticates the user if the credentials are correct.

    Fields:
        - email: The email address of the user.
        - password: The password of the user.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validate the provided email and password. Authenticate the user
        and raise an error if the credentials are invalid.
        """
        email = data.get('email')
        password = data.get('password')

        if email and password:

            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid login credentials")
        else:
            raise serializers.ValidationError("Both fields must be filled")

        data['user'] = user
        return data
