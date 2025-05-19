from django.urls import path
from . import views


urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    
    
    path('admin/signin', views.admin_signin, name='admin_signin'),
    path('admin/signup', views.admin_signup, name='admin_signup'),
    # path('admin/signout', views.admin_signout, name='admin-signout'),
]