from django.contrib import admin
from django.urls import path, include
from join.views import TaskView, DocsView, GenerateDemoDataView, GetCsrfTokenView
from join_contacts.views import ContactView
docs_view = DocsView.as_view({'get': 'get'}) 

urlpatterns = [
    path('docs/', docs_view, name='docs_view'),
    path('admin/', admin.site.urls),
    path('auth/', include('custom_auth.urls')),
    path('contacts/', include('join_contacts.urls')),
    path('task/', TaskView.as_view({'post': 'create', 'get': 'list'})),
    path('task/<int:pk>/', TaskView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'})),
    path('task/<int:pk>/add_subtasks/', TaskView.as_view({'post': 'add_subtasks'})),
    path('task/<int:pk>/subtask/<int:subtask_id>/', TaskView.as_view({'delete': 'remove_subtasks'}), name='remove_subtask'),
    path('task/<int:task_pk>/subtask/<int:subtask_pk>/update/', TaskView.as_view({'patch': 'update_subtask'})),
    path('task/<int:pk>/add_assignees/', TaskView.as_view({'post': 'add_assignees'})),
    path('task/<int:pk>/remove_assignees/', TaskView.as_view({'delete': 'remove_assignees'})),
    path('generate-demo-data/', GenerateDemoDataView.as_view(), name='generate-demo-data'),
    path('get-csrf-token/', GetCsrfTokenView.as_view(), name='get-csrf-token'),
]
