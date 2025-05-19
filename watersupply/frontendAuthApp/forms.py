from django import forms
from django.contrib.auth.password_validation import validate_password

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, min_length=8, validators=[validate_password])
    role = forms.ChoiceField(choices=[('admin', 'Admin'), ('staff', 'Staff')])
    


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    

    
class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, min_length=8, validators=[validate_password])
    phone_number = forms.IntegerField(max_value=9999999999, min_value=1000000000)
    address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    pincode = forms.IntegerField(max_value=999999, min_value=100000)
    
    