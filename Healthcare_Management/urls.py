"""
URL configuration for Healthcare_Management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from Healthcare_Management.admin import admin_site

admin_site.site_header = "Healthcare Management Admin"
admin_site.site_title = "Healthcare Management Admin Portal"
admin_site.index_title = "Welcome to Healthcare Management Dashboard"

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('dashboard.urls')),
    path('patients/', include('patients.urls')),
    path('doctors/', include('doctors.urls')),
    path('appointments/', include('appointments.urls')),
    path('accounts/', include('accounts.urls')),
    path('records/', include('records.urls')),
    path('prescriptions/', include('prescriptions.urls')),
    path('medical_records/', include('medical_records.urls')),
    path('lab_reports/', include('lab_reports.urls')),
    path('billing/', include('billing.urls')),
    path('insurance/', include('insurance.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
