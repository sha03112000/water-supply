from django.shortcuts import render
from authentication.permissions import StaticTokenPermission
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView
from authentication.serializers import AdminLoginTokenSerializer, AdminStaffSerializers, CustomeUsersLoginTokenSerializer, CustomeUsersSerializers
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


# admin/staff login
class CustomeObtainAdminStaffSerializer(TokenObtainPairView):
    permission_classes = [StaticTokenPermission]
    serializer_class = AdminLoginTokenSerializer
    throttle_classes = [AnonRateThrottle]
    
    

    
# user login
class CustomeObtainCustomeUserSerializer(TokenObtainPairView):
    permission_classes = [StaticTokenPermission]
    serializer_class = CustomeUsersLoginTokenSerializer
    throttle_classes = [AnonRateThrottle]
    


# admin/staff register
class CreateAdminStaff(APIView):
    permission_classes = [StaticTokenPermission]
    throttle_classes = [AnonRateThrottle]
    
    def post(self, request, format=None):
        serializer = AdminStaffSerializers(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({
                    'responseStatus': True,
                    'responseData': serializer.data,
                    'responseMessage': 'User created successfully',
                    'responseCode': 200,
                },status=status.HTTP_201_CREATED)
        return Response({
            'responseStatus': False,
            'responseData': serializer.errors,
            'responseMessage': 'User creation failed',
            'responseCode': 400
        })
        

# user register
class CreateCustomeUser(APIView):
    permission_classes = [StaticTokenPermission]
    throttle_classes = [AnonRateThrottle]
    
    def post(self, request, format=None):
        
        try:
            serializers = CustomeUsersSerializers(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response({
                    'responseStatus': True,
                    'responseData': serializers.data,
                    'responseMessage': 'User created successfully',
                    'responseCode': status.HTTP_201_CREATED,
                },status=status.HTTP_201_CREATED)
            return Response({
                'responseStatus': False,
                'responseData': [],
                'responseMessage': serializers.errors,
                'responseCode': status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'responseStatus': False,
                'responseData': [],
                'responseMessage': f'User creation failed: {str(e)}',
                'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR
                # 'res': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


