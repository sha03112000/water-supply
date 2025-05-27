from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from authentication.permissions import StaticTokenPermission

# Create your views here.
class Index(APIView):
    permission_classes = [IsAuthenticated, StaticTokenPermission]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')