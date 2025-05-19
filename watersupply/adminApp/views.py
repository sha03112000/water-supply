from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from authentication.permissions import StaticTokenPermission
from rest_framework.permissions import IsAuthenticated

# Create your views here.



class Index(APIView):
    permission_classes = [StaticTokenPermission, IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    def get(self, request, format=None):
        return Response({'message': 'Hello, World!how are you'}, status=status.HTTP_200_OK)

