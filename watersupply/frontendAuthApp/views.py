from django.shortcuts import render, redirect
from django.conf import settings
import requests
from django.contrib import messages
from frontendAuthApp.forms import RegisterForm, UserRegisterForm
from decouple import config


# helper function for loop errors
def format_error_messages(errors: dict) -> str:
    """
    Convert a dictionary of errors into a formatted string like:
    "username:This field is required, phone_number:Phone number already exists"
    
    Args:
        errors (dict): Dictionary where keys are field names and values are lists of error messages.
    
    Returns:
        str: Formatted error string.
    """
    formatted_errors = []
    for field, messages_list in errors.items():
        message_str = ",".join(messages_list)
        formatted_errors.append(f"{field.capitalize()} : {message_str}")
    return "\n".join(formatted_errors)



# Customer
def signin(request):
    if request.method == 'POST':
        url = f"{config('API_USER_HOST')}/login/"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-STATIC-TOKEN': settings.STATIC_TOKEN
        }
        payload = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password')
        }
        try:
            response = requests.post(url, data=payload, headers=headers)
            data = response.json()

        except (ValueError, requests.exceptions.RequestException):
            messages.error(request, "Login failed. Please try again.")
            return render(request, 'auth/signin.html')
        

        if response.status_code == 200 or response.status_code == 201:
            messages.success(request, data.get('message', 'Login successful!'))
            request.session['user_token'] = data.get('access')
            request.session['refresh'] = data.get('refresh')
            request.session['user_role'] = data.get('role')
            request.session['user_id'] = data.get('user_id')
            request.session['username'] = data.get('username')
            print(response)
            return redirect('index')
        messages.error(request, data.get('detail', 'Login failed. Please try again.'))
    return render(request, 'auth/signin.html')

def signup(request):
    if request.method == 'POST':
        url = f"{config('API_USER_HOST')}/register/"
        
        forms = UserRegisterForm(request.POST)
        if not forms.is_valid():
            # messages.error(request, f"{forms.errors}")
            return render(request, 'auth/signup.html', {'form': forms})
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-STATIC-TOKEN': settings.STATIC_TOKEN
        }
        
        payload = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
            'phone_number': request.POST.get('phone_number'),
            'city': request.POST.get('city'),
            'state': request.POST.get('state'),
            'country': request.POST.get('country'),
            'pincode': request.POST.get('pincode'),
            'address': request.POST.get('address')
        }
        
        try:
            response = requests.post(url, data=payload, headers=headers)
            print(f"Raw response text: {response.text}")
            data = response.json()
            
            if data.get('responseCode') == 201 or data.get('responseStatus') == True:
                messages.success(request, data.get('responseMessage', "Signup successful."))
                return redirect('signin')
            else:
                errors = data.get('responseMessage', {})
                if errors:
                    error_message = format_error_messages(errors)
                    messages.error(request, error_message)
                else:
                    messages.error(request, data.get('responseMessage', 'An error occurred.'))
                return render(request, 'auth/signup.html', {'form': forms})
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Signup failed. Server error: {str(e)}")
            return render(request, 'auth/signup.html', {'form': forms})
    return render(request, 'auth/signup.html', {'form': UserRegisterForm()})


def signout(request):
    request.session.flush()
    messages.success(request, "Logout successful.")
    return redirect('signin')




# Admin
def admin_signin(request):
    if request.method == 'POST':
        url = f"{config('API_ADMIN_HOST')}/login/"
       

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-STATIC-TOKEN': settings.STATIC_TOKEN
        }

        payload = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
        }

        try:
            response = requests.post(url, data=payload, headers=headers)
            data = response.json()
        except (ValueError, requests.exceptions.RequestException):
            print(f"Raw response text: {response.text}")
            messages.error(request, "Login failed. Please try again.")
            return render(request, 'auth/admin-signin.html')

        if response.status_code == 200 or response.status_code == 201:
            messages.success(request, data.get('message', 'Login successful!'))
            request.session['admin_token'] = data.get('access')
            request.session['admin_refresh'] = data.get('refresh')
            request.session['role'] = data.get('role')
            request.session['admin_id'] = data.get('user_id')
            request.session['username'] = data.get('username')
            print(f"Admin token: {request.session['admin_token']}")
            return redirect('admin_index')
        else:
            messages.error(request, data.get('detail', 'Login failed.'))
            return render(request, 'auth/admin-signin.html')
    return render(request, 'auth/admin-signin.html')


def admin_signup(request):
    if request.method == 'POST':
        url = f"{config('API_ADMIN_HOST')}/register/"
        
        forms = RegisterForm(request.POST)

        if not forms.is_valid():
            # messages.error(request, "Signup failed. Please try again.")
            return render(request, 'auth/admin-signup.html', {'form': forms})
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-STATIC-TOKEN': settings.STATIC_TOKEN
        }
        
        payload = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
            'role': request.POST.get('role'),
        }

        try:
            response = requests.post(url, data=payload, headers=headers)
            data = response.json()
            print(f"Raw response text: {response.text}") 
        except (ValueError, requests.exceptions.RequestException):
            messages.error(request, "Signup failed. Please try again.")
            return render(request, 'auth/admin-signup.html', {'form': forms})

        if response.status_code == 200 or response.status_code == 201:
            messages.success(request, data.get('responseMessage', 'Signup successful!'))
            return redirect('admin_signin')
        else:
            messages.error(request, data.get('detail', 'Signup failed.'))
            return render(request, 'auth/admin-signup.html')
    return render(request, 'auth/admin-signup.html', {'form': RegisterForm()})


# def admin_signout(request):
#     return render(request, 'auth/admin-signin.html')
