# users/authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()


class SessionTokenAuthentication(BaseAuthentication):
    """
    Espera header:
        Authorization: Session <uuid-token>
    O header:
        X-Session-Token: <uuid-token>
    """

    def authenticate(self, request):
        auth = request.headers.get("Authorization")
        token = None

        if auth:
            parts = auth.split()
            if len(parts) == 2 and parts[0].lower() == "session":
                token = parts[1]

        if not token:
            token = request.headers.get("X-Session-Token")

        if not token:
            return None  # seguir con otros authenticators (o anon)

        try:
            user = User.objects.get(session_token=token)
        except User.DoesNotExist:
            raise AuthenticationFailed("Token inválido")

        if not user.is_active:
            raise AuthenticationFailed("Usuario inactivo")

        return user, None
