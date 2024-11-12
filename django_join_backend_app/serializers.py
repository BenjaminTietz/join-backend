from rest_framework import serializers
from join.models import Contact, Task, SubTask, TaskContact
from custom_auth.models import User
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate
class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model. Handles the serialization and deserialization
    of contact data, including name, email, phone, initials, and color.

    Fields:
        - id: The contact's ID (auto-generated).
        - name: The name of the contact.
        - email: The email of the contact.
        - phone: The phone number of the contact.
        - initials: The initials of the contact's name.
        - color: A color associated with the contact.
        - created_at: The timestamp when the contact was created.
    """
    class Meta:
        model = Contact
        fields = ('id','name', 'email', 'phone', 'initials', 'color', 'created_at')
    
    def to_representation(self, instance):
        """
        Modify the default representation to include a custom response message.
        """
        data = super().to_representation(instance)
        data['response'] = 'Contact details retrieved successfully.'
        return data
    
class SubTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the SubTask model. Handles the serialization and deserialization
    of subtask data, including title, checked status, and associated task.

    Fields:
        - id: The subtask's ID (auto-generated).
        - title: The title of the subtask.
        - checked: A boolean indicating whether the subtask is completed.
        - created_at: The timestamp when the subtask was created.
        - task: The task to which the subtask is assigned.
    """
    class Meta:
        model = SubTask
        fields = ('id', 'title', 'checked', 'created_at', 'task')        
        
class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model. Handles the serialization and deserialization
    of task data, including title, description, category, priority, status, due date,
    and related subtasks and assigned contacts.

    Fields:
        - id: The task's ID (auto-generated).
        - title: The title of the task.
        - description: The description of the task.
        - category: The category of the task (choice field).
        - priority: The priority of the task (choice field).
        - status: The current status of the task (choice field).
        - dueDate: The due date of the task.
        - subTasks: A list of related subtasks (read-only).
        - assignedTo: A list of contacts assigned to the task (read-only).
    """
    category = serializers.ChoiceField(choices=Task.CATEGORY_CHOICES)
    priority = serializers.ChoiceField(choices=Task.PRIORITY_CHOICES)
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)     
    subTasks = SubTaskSerializer(many=True, read_only=True)  
    assignedTo = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ('id','title', 'description', 'created_at', 'category', 'priority', 'status', 'dueDate', 'subTasks', 'assignedTo')

    def get_assignedTo(self, obj):
        """
        Retrieve all contacts assigned to a task by querying the TaskContact
        model for the current task and returning serialized contact data.
        """
        task_contacts = TaskContact.objects.filter(task=obj)
        contacts = [tc.contact for tc in task_contacts if tc.contact is not None]
        return ContactSerializer(contacts, many=True).data

        
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
