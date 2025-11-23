from datetime import datetime, timedelta
from django.http import HttpResponseForbidden, JsonResponse




class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request
        user = request.user if request.user.is_authenticated else "AnonymmousUser"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        # write logs to a file named requests.log
        with open("requests.log", "a") as f:
            f.write(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # get current hour
        current_hour = datetime.now().hour

        # deny access between 10pm and 6am
        if current_hour >= 22 or current_hour < 6:
            return HttpResponseForbidden("Access denied")

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of chat messages (POST requests) per IP
    within a given time window (e.g., 5 messages per 1 minute).
    """

    # Store message counts per IP
    ip_message_log = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only track POST requests (chat messages)
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize IP data if not exists
            if ip not in self.ip_message_log:
                self.ip_message_log[ip] = []

            # Remove messages older than 1 minute
            one_minute_ago = now - timedelta(minutes=1)
            self.ip_message_log[ip] = [
                timestamp for timestamp in self.ip_message_log[ip] 
                if timestamp > one_minute_ago
            ]

            # Check if limit exceeded
            if len(self.ip_message_log[ip]) >= 5:
                return JsonResponse(
                    {"error": "Message limit exceeded. Please wait before sending more messages."},
                    status=429  # Too Many Requests
                )

            # Record this message timestamp
            self.ip_message_log[ip].append(now)

        # Continue processing request
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get the real client IP from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware:
    """
    Middleware to restrict access to certain actions based on user role.
    Only 'admin' or 'moderator' users are allowed.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Assume that request.user has a 'role' attribute
        user = request.user

        # Only check authenticated users
        if user.is_authenticated:
            allowed_roles = ['admin', 'moderator']
            user_role = getattr(user, 'role', None)

            # Block if role is not allowed
            if user_role not in allowed_roles:
                return HttpResponseForbidden("Access denied: insufficient permissions.")

        # Allow anonymous users to continue (or handle separately)
        response = self.get_response(request)
        return response

