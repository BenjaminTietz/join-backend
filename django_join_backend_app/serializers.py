from rest_framework import serializers
from django.contrib.auth.models import User
from join.models import Contact, Task, SubTask
from phonenumber_field.serializerfields import PhoneNumberField
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')
class ContactSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()
    class Meta:
        model = Contact
        fields = ('id','name', 'email', 'phone')
    def get_phone(self, obj):
        return str(obj.phone) if obj.phone else None
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['response'] = 'Contact details retrieved successfully.'
        data['phone'] = self.get_phone(instance) 
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