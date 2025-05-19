import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect


def call_api(request, url, method='get', data=None,  access_token=None, refresh_token=None, role=None):
    
    access_token_value = access_token
    refresh_token_value = refresh_token
    role_value = role
    headers = {
        'Authorization': f'Bearer {access_token_value}',
        'X-STATIC-TOKEN': settings.STATIC_TOKEN,
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    if method == 'post':
        response = requests.post(url, data=data, headers=headers)
    elif method == 'put':
        response = requests.put(url, data=data, headers=headers)
    elif method == 'delete':
        response = requests.delete(url, data=data, headers=headers)
    elif method == 'patch':
        response = requests.patch(url, data=data, headers=headers)
    else:
        response = requests.get(url, data=data, headers=headers)

    if response.status_code == 401 and refresh_token_value:
        # Try refreshing token
        refresh_url = 'http://192.168.20.3:8000/api/token/refresh/'
        refresh_payload = {'refresh': refresh_token_value}
        refresh_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-STATIC-TOKEN': settings.STATIC_TOKEN
        }

        refresh_response = requests.post(refresh_url, data=refresh_payload, headers=refresh_headers)

        if response.status_code == 200 or response.status_code == 201:
            new_access = refresh_response.json().get('access')
            
            if role_value == 'admin':
                request.session['admin_token'] = new_access
            elif role_value == 'staff':
                request.session['staff_token'] = new_access
            elif role_value == 'customer':
                request.session['customer_token'] = new_access
            
            headers['Authorization'] = f'Bearer {new_access}'

            # Retry original request
            if method == 'post':
                response = requests.post(url, data=data, headers=headers)
            elif method == 'put':
                response = requests.put(url, data=data, headers=headers)
            elif method == 'delete':
                response = requests.delete(url, data=data, headers=headers)
            elif method == 'patch':
                response = requests.patch(url, data=data, headers=headers)
            else:
                response = requests.get(url, headers=headers)
        else:
            messages.error(request, "Session expired. Please log in again.")
            return redirect('signin')
    return response
