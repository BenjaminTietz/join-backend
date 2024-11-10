from django.contrib import admin
from django.urls import path, include
from join.views import ContactView, TaskView, DocsView
from custom_auth.views import LoginView, SignupView
docs_view = DocsView.as_view({'get': 'get'}) 

urlpatterns = [
    path('docs/', docs_view, name='docs_view'),
    path('admin/', admin.site.urls),
    path('auth/', include('custom_auth.urls')),
    path('contact/', ContactView.as_view({'post': 'create', 'get': 'list'})),
    path('contact/<int:pk>/', ContactView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('task/', TaskView.as_view({'post': 'create', 'get': 'list'})),
    path('task/<int:pk>/', TaskView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'})),
    path('task/<int:pk>/add_subtasks/', TaskView.as_view({'post': 'add_subtasks'})),
    path('task/<int:pk>/subtask/<int:subtask_id>/', TaskView.as_view({'delete': 'remove_subtasks'}), name='remove_subtask'),
    path('task/<int:task_pk>/subtask/<int:subtask_pk>/update/', TaskView.as_view({'patch': 'update_subtask'})),
    path('task/<int:pk>/add_assignees/', TaskView.as_view({'post': 'add_assignees'})),
    path('task/<int:pk>/remove_assignees/', TaskView.as_view({'delete': 'remove_assignees'})),
]
