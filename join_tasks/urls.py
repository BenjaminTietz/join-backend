from django.urls import path
from join.views import TaskView

urlpatterns = [
    path('', TaskView.as_view({'post': 'create', 'get': 'list'}), name='task-list-create'),
    path('<int:pk>/', TaskView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'}), name='task-detail'),
    path('<int:pk>/add_subtasks/', TaskView.as_view({'post': 'add_subtasks'}), name='task-add-subtasks'),
    path('<int:pk>/subtask/<int:subtask_id>/', TaskView.as_view({'delete': 'remove_subtasks'}), name='task-remove-subtask'),
    path('<int:task_pk>/subtask/<int:subtask_pk>/update/', TaskView.as_view({'patch': 'update_subtask'}), name='task-update-subtask'),
    path('<int:pk>/add_assignees/', TaskView.as_view({'post': 'add_assignees'}), name='task-add-assignees'),
    path('<int:pk>/remove_assignees/', TaskView.as_view({'delete': 'remove_assignees'}), name='task-remove-assignees'),
]