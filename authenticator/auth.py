from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    """
    Read access token from HttpOnly cookie instead of Authorization header
    """
    def authenticate(self, request):
        raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        
        if raw_token is None:
            return super().authenticate(request)

        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
        except Exception as e:
            raise AuthenticationFailed(str(e))

        return (user, validated_token)
