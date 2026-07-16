import requests as http_requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

from powerUp.models import Cliente
from powerUp.views.LoginView import _set_auth_cookies

GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


class GoogleLoginView(APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.data.get('access_token')

        if not access_token:
            return Response(
                {'detail': 'access_token é obrigatório.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # --- 1. Obter dados do usuário via Google userinfo endpoint ---
        try:
            userinfo_response = http_requests.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10,
            )
            userinfo_response.raise_for_status()
            userinfo = userinfo_response.json()
        except Exception as e:
            return Response(
                {'detail': f'Não foi possível validar o token Google: {str(e)}'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        email = userinfo.get('email')

        if not email:
            return Response(
                {'detail': 'Não foi possível obter o e-mail da conta Google.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        nome = (
            userinfo.get('name')
            or userinfo.get('given_name')
            or email.split('@')[0]
        )

        # --- 2. Buscar ou criar o User do Django ---
        # Busca por username=email (username é o campo único do Django Auth)
        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                'email': email,
                'first_name': nome,
            }
        )

        if created:
            user.set_unusable_password()
            user.save(update_fields=['password'])

        # --- 3. Buscar ou criar o Cliente vinculado ---
        cliente, _ = Cliente.objects.get_or_create(
            user=user,
            defaults={
                'nome': nome,
                'perfil': 'user',
            }
        )

        # --- 4. Gerar tokens JWT ---
        refresh = RefreshToken.for_user(user)
        jwt_access = str(refresh.access_token)
        jwt_refresh = str(refresh)

        # --- 5. Montar resposta (mesmo formato do login normal) ---
        data = {
            'id': cliente.id,
            'nome': cliente.nome,
            'email': user.email,
            'perfil': cliente.perfil,
            'has_password': user.has_usable_password(),
        }

        response = Response(data, status=status.HTTP_200_OK)

        # --- 6. Setar cookies HttpOnly (reutiliza helper do LoginView) ---
        _set_auth_cookies(response, jwt_access, jwt_refresh)

        return response
