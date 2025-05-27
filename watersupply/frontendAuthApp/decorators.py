from django.shortcuts import redirect
from django.contrib import messages

def login_required_decorator(view_func):
    def _wrapped_view(request, *args, **kwargs):
        
        token = request.session.get('user_token')
        role = request.session.get('user_role')
        if not token or role != 'user':
            messages.error(request, 'please log in to continue.')
            return redirect('signin')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


