from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import TokenError


class CustomTokenAuthentication(TokenAuthentication):

    def authenticate(self, request):
        # Get the header from the request
        header = self.get_header(request)
        if header is None:
            return None

        # Get the token from the header
        token = self.get_token(header)
        # If the token is not found, raise an authentication failed exception
        if token is None:
            raise AuthenticationFailed("Token is required")
        try:
            # Validate the token
            validated_token = self.validate_token(token) 
            # Get the user from the token
            user = self.get_user(validated_token)
            # If the user is not found, raise an authentication failed exception
            if user is None:
                raise AuthenticationFailed("User not found")
            return (user, validated_token)
        # If the token is invalid, raise an authentication failed exception
        except TokenError as e:
            raise AuthenticationFailed("Invalid token")
        # If there is an error, raise an authentication failed exception
        except Exception as e:
            raise AuthenticationFailed("Error authenticating token")
     