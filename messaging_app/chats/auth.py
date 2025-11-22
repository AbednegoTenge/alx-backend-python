from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class CustomTokenAuthentication(JWTAuthentication):

    def authenticate(self, request):
        """
        Custom authentication flow for JWT.
        """
        # Get header: e.g. "Bearer <token>"
        header = self.get_header(request)
        if header is None:
            return None  # No token sent → DRF treats it as "unauthenticated"

        # Extract raw token
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            raise AuthenticationFailed("Token is missing")

        try:
            # Validate and decode
            validated_token = self.get_validated_token(raw_token)
            # Get user from the decoded token
            user = self.get_user(validated_token)

            if user is None:
                raise AuthenticationFailed("User not found")

            return (user, validated_token)

        except TokenError:
            raise AuthenticationFailed("Invalid or expired token")

        except InvalidToken:
            raise AuthenticationFailed("Token validation error")

        except Exception:
            raise AuthenticationFailed("Authentication failed")
