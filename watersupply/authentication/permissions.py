from rest_framework.permissions import BasePermission
from django.conf import settings


class StaticTokenPermission(BasePermission):
    STATIC_ACCESS_TOKEN = settings.STATIC_TOKEN
    
    def has_permission(self, request, view):
        token = request.headers.get('X-STATIC-TOKEN') #key for the static token in headers
        return token == self.STATIC_ACCESS_TOKEN