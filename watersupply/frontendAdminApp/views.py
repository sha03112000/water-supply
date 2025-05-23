from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from utils.api_call import call_api
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import json
import requests
from decouple import config
# Create your views here.

def get_admin_tokens(request):
    return {
        'access_token': request.session.get('admin_token'),
        'refresh_token': request.session.get('admin_refresh'),
        'role': request.session.get('role'),
    }

        
        
def admin_index(request):
    tokens = get_admin_tokens(request)
    url = f"{config('API_ADMIN_HOST')}/index/"
    
    
    response = call_api(
        request,
        url,
        method='get',
        access_token=tokens['access_token'],
        refresh_token=tokens['refresh_token'],
        role=tokens['role'],
    )

    if isinstance(response, HttpResponseRedirect):
        return response

    print(f"Raw response text: {response.text}")  # Helps in debugging


    try:
        data = response.json()
    except json.JSONDecodeError:
        return HttpResponse("Invalid or empty JSON response from API", status=502)

    return JsonResponse(data, status=response.status_code, safe=False)