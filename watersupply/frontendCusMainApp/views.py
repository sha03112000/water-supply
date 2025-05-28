from django.shortcuts import render, redirect
from django.http import HttpResponse
from frontendAuthApp.decorators import login_required_decorator
from utils.api_call import call_api
from django.conf import settings
from decouple import config
from django.http import HttpResponseRedirect
from django.contrib import messages


# Create your views here.
def get_user_tokens(request):
    return {
        'access_token': request.session.get('user_token'),
        'refresh_token': request.session.get('refresh'),
        'role': request.session.get('user_role'),
    }

@login_required_decorator
def index(request):
    token = get_user_tokens(request)
    
    url = f"{config('API_USER_HOST')}/dashboard/"
    
    response = call_api(
        request,
        url,
        method='get',
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        role=token['role'],
    )
    
    # If the call_api function returned a redirect to  'signin'
    if isinstance(response, HttpResponseRedirect):  
        return response

    if response.status_code == 401:
        print(f"Raw response text: {response.text}")
        messages.error(request, "session expired, please login again.")
        return redirect('signout')
       
    try:
        data = response.json()
    except ValueError:
        messages.error(request,  "Invalid response from server.")
        return render(request, 'user/index.html', {'data': {}})

    # Normal case
    if not data.get('responseStatus', False):
        messages.error(request, data.get('responseMessage', "Failed to fetch dashboard."))
        return render(request, 'user/index.html', {'data': {}})
    messages.success(request, data.get('responseMessage', "Dashboard fetched successfully"))
    products = data.get('responseData', {}).get('products', [])
    return render(request, 'user/index.html', {'data': products})
