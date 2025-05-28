import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from decouple import config


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
        refresh_url = config('API_TOKEN_REFRESH')
        refresh_payload = {'refresh': refresh_token_value}
        # print('refresh_payload',refresh_payload)
        refresh_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-STATIC-TOKEN': settings.STATIC_TOKEN
        }

        refresh_response = requests.post(refresh_url, data=refresh_payload, headers=refresh_headers)

        if refresh_response.status_code in [200, 201]:
            new_access = refresh_response.json().get('access')
            
            if role_value == 'admin':
                request.session['admin_token'] = new_access
            elif role_value == 'staff':
                request.session['staff_token'] = new_access
            elif role_value == 'user':
                request.session['user_token'] = new_access

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
