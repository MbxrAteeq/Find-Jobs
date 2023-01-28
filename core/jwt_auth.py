import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from user.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = "Bearer"

    def has_permission(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()
        if not auth_header or len(auth_header) == 1 or len(auth_header) > 2:
            return None
        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")
        if prefix.lower() != auth_header_prefix:
            return None
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        Return the user and token if authentication is successful,
        If authentication fails, throw an error.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except:
            msg = "Invalid authentication. Could not decode token."
            raise exceptions.AuthenticationFailed(msg)
        try:
            user = User.objects.get(pk=payload["user_id"])
        except User.DoesNotExist:
            msg = "No user matching this token was found."
            raise exceptions.AuthenticationFailed(msg)
        if not user.is_active:
            msg = "This user has been deactivated."
            raise exceptions.AuthenticationFailed(msg)
        request.user = user
        return user, token

    def authenticate(self, request):
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        if not auth_token:
            return
        auth_token = auth_token.split(' ')[1]
        return self._authenticate_credentials(request, auth_token)
