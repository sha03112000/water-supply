from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from authentication.permissions import StaticTokenPermission
from rest_framework.response import Response
from rest_framework import status

# call class ProductsListAndCreate from adminApp.views
from adminApp.views import  ProductsListAndCreate



productFetch  = ProductsListAndCreate()

# Create your views here.
class Index(APIView):
    permission_classes = [IsAuthenticated, StaticTokenPermission]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    paginator_class = productFetch.pagination_class
    serializer_class = productFetch.serializer_class
    parser_classes = productFetch.parser_classes
    # This class is used to fetch the products for the customer dashboard
    def get(self, request, format=None):
        products = productFetch.get(request, format=format)
        return Response({
            'responseStatus': True,
            'responseData': {
                'pagination': products.data['responseData']['pagination'],
                'products': products.data['responseData']['products'],
                'myOrders': [],
            },
            'responseMessage': 'Dashboard results fetched successfully',
            'responseCode': status.HTTP_200_OK
        }, status= status.HTTP_200_OK)

        