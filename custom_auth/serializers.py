from rest_framework import serializers
from join_tasks.models import Task, SubTask, TaskContact
from join_contacts.models import Contact
from custom_auth.models import User
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate
from rest_framework import serializers
from custom_auth.models import User
from datetime import date
from rest_framework import serializers
from custom_auth.models import User
from django.contrib.auth.password_validation import validate_password
from join_contacts.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'created_at', 'initials', 'color' ]
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password]) 
    created_at = serializers.DateTimeField(read_only=True)
    phone = serializers.CharField(required=True)
    contact = ContactSerializer(source='contact_id', read_only=True)  

    def create(self, validated_data):
        """
        Erstelle einen neuen Benutzer mit den übergebenen Daten.
        Der Benutzer gibt seinen vollständigen Namen direkt als `username` an.
        """
        user = User(
            username=validated_data['username'],  
            email=validated_data['email'],       
            phone=validated_data.get('phone', ''),
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'created_at', 'password', 'contact')


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login. Validates the provided email and password,
    and authenticates the user if the credentials are correct.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid login credentials")
        else:
            raise serializers.ValidationError("Both fields must be filled")

        data['user'] = user
        data['contact_id'] = user.contact_id_id  
        data['contact'] = Contact.objects.filter(id=user.contact_id_id).first()

        return data

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)