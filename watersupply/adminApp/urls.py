from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductsListAndCreate.as_view(), name='admin_products'),
    path('products/<int:pk>/', views.ProductsRetrieveUpdateDelete.as_view(), name='admin_product_detail'),
]