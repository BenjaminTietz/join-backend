from .models import Task, SubTask, Contact
from django.contrib import admin

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'category', 'priority', 'status', 'due_date', 'created_at')
    fields = ('id', 'title', 'description', 'category', 'priority', 'status', 'due_date', 'created_at')
    readonly_fields = ('id', 'created_at')  
admin.site.register(SubTask)
admin.site.register(Contact)
