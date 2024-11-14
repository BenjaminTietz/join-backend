from rest_framework import serializers
from join_tasks.models import Task, SubTask, TaskContact
from join_contacts.models import Contact
from custom_auth.models import User
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate
from rest_framework import serializers
from custom_auth.models import User
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at

    def create(self, validated_data):
        user = User(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            real_name=validated_data.get('real_name')  
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'real_name', 'created_at', 'password')


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
