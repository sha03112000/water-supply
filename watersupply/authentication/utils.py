from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled

def custom_exception_handler(exc, context):
    
    response = exception_handler(exc, context)

    if isinstance(exc, Throttled):
        custom_response_data = { 
            'detail': 'Too many requests.',
            'retry_after': f'{exc.wait} seconds',
            'error_code': '429'
        }
        response.data = custom_response_data 
    return response