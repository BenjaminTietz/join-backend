from rest_framework import serializers
from django.contrib.auth.models import User
from join.models import Contact, Task, SubTask
from phonenumber_field.serializerfields import PhoneNumberField
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id','name', 'email', 'phone')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['response'] = 'Contact details retrieved successfully.'
        return data
        
class TaskSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Task.CATEGORY_CHOICES)
    priority = serializers.ChoiceField(choices=Task.PRIORITY_CHOICES)
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)
    class Meta:
        model = Task
        fields = ('title', 'description', 'created_at', 'category', 'priority', 'status', 'due_date')

    def create(self, validated_data):
        return Task.objects.create(**validated_data)
    
class SubTaskSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    class Meta:
        model = SubTask
        fields = ('task','title', 'checked', 'created_at')