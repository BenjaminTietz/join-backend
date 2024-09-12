from .models import Task, SubTask, Contact
from django.contrib import admin

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'category', 'priority', 'status', 'due_date', 'created_at')
    fields = ('id', 'title', 'description', 'category', 'priority', 'status', 'due_date', 'created_at')
    readonly_fields = ('id', 'created_at')  
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
