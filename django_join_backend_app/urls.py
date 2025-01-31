from django.contrib import admin
from django.urls import path, include
from join.views import DocsView, GenerateDemoDataView, GetCsrfTokenView
from join_contacts.views import ContactView
docs_view = DocsView.as_view({'get': 'get'}) 

urlpatterns = [
    path('docs/', docs_view, name='docs_view'),
    path('admin/', admin.site.urls),
    path('', include('custom_auth.urls')),
    path('contacts/', include('join_contacts.urls')),
    path('task/', include('join_tasks.urls')),
    path('generate-demo-data/', GenerateDemoDataView.as_view(), name='generate-demo-data'),
    path('get-csrf-token/', GetCsrfTokenView.as_view(), name='get-csrf-token'),
]
