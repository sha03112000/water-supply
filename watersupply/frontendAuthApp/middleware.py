from django.shortcuts import redirect
from django.contrib import messages


class AdminRoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith('/admin/') and not path.startswith('/admin/signin') and not path.startswith('/admin/signup'):
            token = request.session.get('admin_token')
            role = request.session.get('role')
            if not token or role != 'admin':
                messages.error(request, "Access denied.")
                return redirect('admin_signin')
        return self.get_response(request)

