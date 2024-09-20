from .models import Task, SubTask, Contact, User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
# Register your models here.
class SubTaskInline(admin.TabularInline): 
    model = SubTask
    extra = 1 
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'category', 'priority', 'status', 'due_date', 'created_at')
    fields = ('id', 'title', 'description', 'category', 'priority', 'status', 'due_date', 'created_at')
    readonly_fields = ('id', 'created_at')  
    inlines = [SubTaskInline]
@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'title', 'checked', 'created_at')
    fields = ('id', 'task', 'title', 'checked', 'created_at')
    readonly_fields = ('id', 'created_at')
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'created_at')
    fields = ('id', 'name', 'email', 'phone', 'created_at')
    readonly_fields = ('id', 'created_at')

@admin.register(User)
class UserAdmin(BaseUserAdmin):

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