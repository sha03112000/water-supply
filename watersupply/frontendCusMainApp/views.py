from django.shortcuts import render
from django.http import HttpResponse
from frontendAuthApp.decorators import login_required_decorator


# Create your views here.

@login_required_decorator
def index(request):
    return HttpResponse("Welcome You are logged In as a Customer")