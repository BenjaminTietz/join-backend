from rest_framework import serializers
from join.models import Contact, Task, SubTask, User
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User  (
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
        fields = ('id','name', 'email', 'phone', 'initials', 'color', 'created_at')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['response'] = 'Contact details retrieved successfully.'
        return data
class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('id', 'title', 'checked', 'created_at', 'task')        
class TaskSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Task.CATEGORY_CHOICES)
    priority = serializers.ChoiceField(choices=Task.PRIORITY_CHOICES)
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)     
    subTasks = SubTaskSerializer(many=True, read_only=True)  
    class Meta:
        model = Task
        fields = ('id','title', 'description', 'created_at', 'category', 'priority', 'status', 'dueDate', 'subTasks')

    def create(self, validated_data):
        return Task.objects.create(**validated_data)
    

        
class LoginSerializer(serializers.Serializer):
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
        return data
