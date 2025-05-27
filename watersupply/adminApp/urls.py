from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductsListAndCreate.as_view(), name='admin_products'),
]