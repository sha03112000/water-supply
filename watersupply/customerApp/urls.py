from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.Index.as_view(), name='customer_dashboard'),
]