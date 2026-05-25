from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        # Invalida o refresh token na blacklist (se existir e for válido)
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass

        response = Response({'detail': 'Logout realizado com sucesso.'}, status=status.HTTP_200_OK)

        response.delete_cookie('access', path='/')
        response.delete_cookie('refresh', path='/')

        return response
