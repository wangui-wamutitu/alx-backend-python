import logging
from datetime import datetime
from django.http import JsonResponse, HttpResponseForbidden


request_logger = logging.getLogger("request_logger")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = (
            request.user
            if hasattr(request, "user") and request.user.is_authenticated
            else "Anonymous"
        )
        request_logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time
        # Assumes prompt means access denied from 9pm to 6am
        if not (
            datetime.strptime("06:00", "%H:%M").time()
            <= current_time
            < datetime.strptime("21:00", "%H:%M").time()
        ):
            return HttpResponseForbidden("Access to chat is from 9pm to 6am.")

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_log = {}

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/api/messages/"):
            ip = self.get_client_ip(request)
            now = datetime.time()

            timestamps = self.ip_message_log.get(ip, [])
            timestamps = [ts for ts in timestamps if now - ts < 60]

            if len(timestamps) >= 5:
                return JsonResponse(
                    {
                        "error": "Rate limit exceeded. Only 5 messages allowed per minute."
                    },
                    status=429,
                )

            timestamps.append(now)
            self.ip_message_log[ip] = timestamps

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get the client IP address from the request."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        if user and user.is_authenticated:
            protected_paths = ["/api/messages/", "/api/conversations/"]
            if any(request.path.startswith(path) for path in protected_paths):
                if user.role not in ["admin", "moderator"]:
                    request_logger.warning(
                        f"Access denied for user {user.email} with role '{user.role}' to path {request.path}"
                    )
                    return HttpResponseForbidden(
                        "You do not have permission to perform this action."
                    )

        response = self.get_response(request)
        return response
