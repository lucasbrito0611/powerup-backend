from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from powerUp.views.LoginView import _set_auth_cookies

User = get_user_model()


class RefreshCookieView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token_str = request.COOKIES.get('refresh')

        if not refresh_token_str:
            return Response(
                {'detail': 'Refresh token ausente.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            # Valida assinatura, expiração e verifica na blacklist
            token = RefreshToken(refresh_token_str)
            user_id = token.payload.get('user_id')
            user = User.objects.get(id=user_id)

            # Invalida o refresh token atual na blacklist
            token.blacklist()

            # Gera novo par de tokens para o usuário
            new_refresh = RefreshToken.for_user(user)
            new_access = str(new_refresh.access_token)

            response = Response({'detail': 'Token renovado.'}, status=status.HTTP_200_OK)
            _set_auth_cookies(response, new_access, str(new_refresh))
            return response

        except User.DoesNotExist:
            response = Response(
                {'detail': 'Usuário não encontrado.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            response.delete_cookie('access', path='/')
            response.delete_cookie('refresh', path='/')
            return response

        except (TokenError, InvalidToken):
            # Refresh inválido/expirado — apaga os cookies para forçar novo login
            response = Response(
                {'detail': 'Sessão expirada. Faça login novamente.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            response.delete_cookie('access', path='/')
            response.delete_cookie('refresh', path='/')
            return response
