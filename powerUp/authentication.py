from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken


class JWTCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Tenta ler o token do cookie HttpOnly primeiro
        raw_token = request.COOKIES.get('access')

        if raw_token is None:
            # Sem cookie — usuário não autenticado (não é erro)
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except (InvalidToken, TokenError):
            # Cookie presente mas token inválido/expirado
            return None

        return self.get_user(validated_token), validated_token
