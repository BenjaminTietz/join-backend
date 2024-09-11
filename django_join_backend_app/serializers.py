from rest_framework import serializers
from django.contrib.auth.models import User
from join.models import Contact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone')