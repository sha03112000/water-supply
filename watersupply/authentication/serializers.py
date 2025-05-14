from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken



# admin/staff register


User = get_user_model()
class AdminStaffSerializers(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    role = serializers.ChoiceField(
        choices=[('admin', 'Admin'), ('staff', 'Staff')],
        required=True,
        write_only=True 
    )
    

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):
        role = validated_data.pop('role', 'staff')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.is_staff = True
        if role == 'admin':
            user.is_superuser = True
        user.save()
        return user



# admin/staff login
class AdminLoginTokenSerializer(TokenObtainPairSerializer):
    
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        
        if not user.is_active or not user.is_staff:
            raise AuthenticationFailed("Not authorized as staff or admin.")
        
        data['role'] = 'admin' if user.is_superuser else 'staff'
        data['username'] = user.username
        data['user_id'] = user.id
        data['username'] = user.username
        data['message'] = f"Login successful for {data['role']}."

        return data
    



# customer register
class CustomeUsersSerializers(serializers.ModelSerializer):
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    phone_number = serializers.IntegerField(required=True)
    address = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    country = serializers.CharField(required=True)
    pincode = serializers.IntegerField(required=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'phone_number', 'address', 'city', 'state', 'country', 'pincode']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
        #hash password
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
# customer login

class CustomeUsersLoginTokenSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid credentials.')

        if not user.check_password(password):
            raise AuthenticationFailed('Invalid credentials.')

        if not user.is_active:
            raise AuthenticationFailed('User is inactive.')

        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': 'user',
            'user_id': user.id,
            'username': user.username,
            'message': 'Login successful for user.'
        }
        