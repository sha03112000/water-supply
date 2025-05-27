from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from authentication.permissions import StaticTokenPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from . serializers import ProductSerializer, OrderSerializer
from . models import Products, Orders

# Create your views here.
class Paginations(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductsListAndCreate(APIView):
    permission_classes = [IsAuthenticated, StaticTokenPermission]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    pagination_class = Paginations
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProductSerializer
    
    def get(self, request, format=None):
        try:
            paginator = self.pagination_class()
            
            all_products = Products.objects.all().order_by('-created_at')
            paginated_products = paginator.paginate_queryset(all_products, request)
            product_serializer = self.serializer_class(paginated_products, many=True, context={'request': request})
            pagination_data = paginator.get_paginated_response(product_serializer.data).data

            return Response({
                'responseStatus': True,
                'responseData': {
                    'pagination': {
                        'count': pagination_data['count'],
                        'next': pagination_data['next'],
                        'previous': pagination_data['previous'],
                    },
                    'products': pagination_data['results'],
                    
                },
                'responseMessage': 'Products fetched successfully',
                'responseCode': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'responseStatus': False,
                'responseData': {
                    'products': []
                },
                'responseMessage': f"'Error occurred while fetching products': {str(e)}",
                'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def post(self, request, format=None):
        try:
            product_serializer = self.serializer_class(data=request.data)
            if product_serializer.is_valid():
                product_serializer.save(created_by=request.user, updated_by=request.user)
                return Response({
                    'responseStatus': True,
                    'responseData': product_serializer.data,
                    'responseMessage': 'Product created successfully',
                    'responseCode': status.HTTP_201_CREATED
                }, status=status.HTTP_201_CREATED)
            return Response({
                'responseStatus': False,
                'responseData': [],
                'responseMessage': product_serializer.errors,
                'responseCode': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'responseStatus': False,
                'responseData': {},
                'responseMessage': str(e),
                'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class ProductsRetrieveUpdateDelete(APIView):
    permission_classes = [IsAuthenticated, StaticTokenPermission]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProductSerializer
    
    def get(self, request, pk, format=None):
        try:
            product = Products.objects.get(pk=pk)
            product_serializer = self.serializer_class(product, context={'request': request}).data
            return Response({
                'responseStatus': True,
                'responseData': {
                    'product': product_serializer
                },
                'responseMessage': 'Product fetched successfully',
                'responseCode': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Products.DoesNotExist:
            return Response({
                'responseStatus': False,
                'responseData': {
                    'product': {}
                },
                'responseMessage': 'Product not found',
                'responseCode': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'responseStatus': False,
                'responseData': {
                    'product': {}
                },
                'responseMessage': f'Error occurred while fetching product: {str(e)}',
                'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk, format=None):
        try:
            product = Products.objects.get(pk=pk)
            product_serializer = self.serializer_class(product, data=request.data, partial=True)
            if product_serializer.is_valid():
                product_serializer.save(updated_by=request.user)
                return Response({
                    'responseStatus': True,
                    'responseData': product_serializer.data,
                    'responseMessage': 'Product updated successfully',
                    'responseCode': status.HTTP_200_OK
                }, status=status.HTTP_200_OK)
            return Response({
                'responseStatus': False,
                'responseData': [],
                'responseMessage': product_serializer.errors,
                'responseCode': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
        except Products.DoesNotExist:
            return Response({
                'responseStatus': False,
                'responseData': {},
                'responseMessage': 'Product not found',
                'responseCode': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'responseStatus': False,
                'responseData': {},
                'responseMessage': f'Error occurred while updating product: {str(e)}',
                'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR 
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def delete(self, request, pk, format=None):
        try:
            product = Products.objects.get(pk=pk , created_by=request.user)
            # Ensure the product is created by the authenticated user
            product.delete()
            return Response({
                'responseStatus': True,
                'responseData': {},
                'responseMessage': 'Product deleted successfully',
                'responseCode': status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_204_NO_CONTENT)
        except Products.DoesNotExist:
            return Response({
                'responseStatus': False,
                'responseData': {},
                'responseMessage': 'Product not found or you do not have permission to delete it',
                'responseCode': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'responseStatus': False,
                'responseData': {},
                'responseMessage': f'Error occurred while deleting product: {str(e)}',
                'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    

    
