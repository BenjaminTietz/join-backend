"""
URL configuration for django_join_backend_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from join.views import LoginView, SignupView, ContactView, TaskView, SubTaskView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('signup/', SignupView.as_view({'post': 'create'})),
    path('contact/', ContactView.as_view({'post': 'create'})),
    path('task/', TaskView.as_view({'post': 'create'})),
    path('task/<int:pk>/', TaskView.as_view({'get': 'retrieve'})),
    path('subTask/', SubTaskView.as_view({'post': 'create'})),
]
