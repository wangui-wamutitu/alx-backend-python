import logging
from datetime import datetime
from rest_framework.exceptions import HttpResponseForbidden


request_logger = logging.getLogger('request_logger')


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else "Anonymous"
        request_logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time
        # Assumes prompt means access denied from 9pm to 6am
        if not (datetime.strptime("06:00", "%H:%M").time() <= current_time < datetime.strptime("21:00", "%H:%M").time()):
            return HttpResponseForbidden("Access to chat is from 9pm to 6am.")
        
        response = self.get_response(request)
        return response
    