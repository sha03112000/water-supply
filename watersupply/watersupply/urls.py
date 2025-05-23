"""
URL configuration for watersupply project.

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
from django.contrib import admin
from django.urls import path,include

from authentication.views import CreateAdminStaff, CreateCustomeUser, CustomeObtainAdminStaffSerializer, CustomeObtainCustomeUserSerializer
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # path('admin/', admin.site.urls),
    
    path('api/admin/register/', CreateAdminStaff.as_view(), name='create-admin-staff'),
    path('api/admin/login/',CustomeObtainAdminStaffSerializer.as_view(),name='admin-login'),
    
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # for both admin/staff and user
    
    path('api/user/register/', CreateCustomeUser.as_view(), name='create-user'),
    path('api/user/login/',CustomeObtainCustomeUserSerializer.as_view(),name='user-login'),
    
    path('api/admin/', include('adminApp.urls')),
    
    # frontend
    path('', include('frontendCusMainApp.urls')),
    path('auth/', include('frontendAuthApp.urls')),
    path('admin/', include('frontendAdminApp.urls')),
]
