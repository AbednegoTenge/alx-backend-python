from datetime import datetime


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