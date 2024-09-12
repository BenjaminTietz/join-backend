from rest_framework import serializers
from django.contrib.auth.models import User
from join.models import Contact, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone')
        
class TaskSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Task.CATEGORY_CHOICES)
    priority = serializers.ChoiceField(choices=Task.PRIORITY_CHOICES)
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)
    class Meta:
        model = Task
        fields = ('title', 'description', 'created_at', 'category', 'priority', 'status', 'due_date')

    def create(self, validated_data):
        return Task.objects.create(**validated_data)