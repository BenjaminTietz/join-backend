from django.urls import path
from .views import ContactView

urlpatterns = [
    path('', ContactView.as_view({'post': 'create', 'get': 'list'}), name='contact-list'),
    path('<int:pk>/', ContactView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'}), name='contact-detail'),
]