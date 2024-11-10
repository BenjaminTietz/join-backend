from .models import Task, SubTask, Contact
from custom_auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _


#admin.site.register(User)

class SubTaskInline(admin.TabularInline): 
    """
    Inline admin class for the SubTask model. 
    Allows SubTasks to be managed directly within the Task admin page.
    
    Fields:
        - model: The related SubTask model.
        - extra: The number of empty forms displayed in the inline.
    """
    model = SubTask
    extra = 1 
    
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Task model instances. 
    Displays task information, handles readonly fields, and includes 
    inline management of related SubTasks.

    List Display:
        - id: The unique identifier of the task.
        - title: The title of the task.
        - description: A brief description of the task.
        - category: The category of the task.
        - priority: The priority level of the task.
        - status: The current status of the task.
        - dueDate: The due date for the task.
        - created_at: The timestamp when the task was created.

    Fields:
        - id: The unique identifier of the task (readonly).
        - title: The title of the task.
        - description: A brief description of the task.
        - category: The category of the task.
        - priority: The priority level of the task.
        - status: The current status of the task.
        - dueDate: The due date for the task.
        - created_at: The timestamp when the task was created (readonly).
    """
    list_display = ('id', 'title', 'description', 'category', 'priority', 'status', 'dueDate', 'created_at')
    fields = ('id', 'title', 'description', 'category', 'priority', 'status', 'dueDate', 'created_at')
    readonly_fields = ('id', 'created_at')  
    inlines = [SubTaskInline]
    
    def get_assignees(self, obj):
        """
        Returns a comma-separated string of assignees for the task.
        """
        return ", ".join([str(contact) for contact in obj.assignees.all()])
    get_assignees.short_description = 'Assignees'
    
@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    """
    Admin interface for managing SubTask model instances.
    
    List Display:
        - id: The unique identifier of the subtask.
        - task: The task that this subtask is related to.
        - title: The title of the subtask.
        - checked: A boolean indicating whether the subtask is completed.
        - created_at: The timestamp when the subtask was created.
    
    Fields:
        - id: The unique identifier of the subtask (readonly).
        - task: The related task of the subtask.
        - title: The title of the subtask.
        - checked: A boolean indicating the completion status of the subtask.
        - created_at: The timestamp when the subtask was created (readonly).
    """
    list_display = ('id', 'task', 'title', 'checked', 'created_at')
    fields = ('id', 'task', 'title', 'checked', 'created_at')
    readonly_fields = ('id', 'created_at')
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Contact model instances.
    
    List Display:
        - id: The unique identifier of the contact.
        - name: The name of the contact.
        - email: The email of the contact.
        - phone: The phone number of the contact.
        - created_at: The timestamp when the contact was created.
        - initials: The initials of the contact's name.
        - color: A color associated with the contact.
    
    Fields:
        - id: The unique identifier of the contact (readonly).
        - name: The name of the contact.
        - email: The email of the contact.
        - phone: The phone number of the contact.
        - created_at: The timestamp when the contact was created (readonly).
        - initials: The initials of the contact.
        - color: A color associated with the contact.
    """
    list_display = ('id', 'name', 'email', 'phone', 'created_at', 'initials', 'color')
    fields = ('id', 'name', 'email', 'phone', 'created_at', 'initials', 'color')
    readonly_fields = ('id', 'created_at')

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin interface for managing User model instances.
    
    List Display:
        - email: The user's email address.
        - username: The username of the user.
        - is_staff: A boolean indicating whether the user has staff permissions.
        - is_active: A boolean indicating whether the user account is active.
    
    Fieldsets:
        - Personal info: Fields related to the user's personal information.
        - Permissions: Fields related to user permissions and access control.
        - Important dates: Fields related to important timestamps (e.g., last login).
    
    Add Fieldsets:
        - A wide format layout for adding a new user, including password fields.
    
    Additional Configurations:
        - search_fields: Allows searching by email and username.
        - ordering: Orders users by email in the admin interface.
        - filter_horizontal: Provides horizontal filters for managing groups and permissions.
    """
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')


    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username',)}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)