from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from powerUp.authentication import JWTCookieAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import status
from powerUp.models import Cliente


class EmailTokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Tenta buscar o usuário pelo email
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Email ou senha incorretos.")

        # Autentica usando username, senha e o request para o django-axes
        request = self.context.get('request')
        user = authenticate(request=request, username=user_obj.username, password=password)
        if not user:
            raise serializers.ValidationError("Email ou senha incorretos.")

        # Gera tokens JWT
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        # Pega dados do cliente
        try:
            cliente = user.cliente
            cliente_id = cliente.id
            nome = cliente.nome
            perfil = cliente.perfil

        except Exception:
            nome = user.username
            perfil = 'user'
            cliente_id = None

        # Tokens são retornados internamente mas serão escritos como cookies pela view.
        # Apenas dados de perfil ficam no body JSON (sem tokens sensíveis).
        return {
            '_refresh_token': str(refresh),
            '_access_token': access,
            'id': cliente_id,
            'nome': nome,
            'email': user.email,
            'perfil': perfil,
            'has_password': user.has_usable_password(),
        }


def _set_auth_cookies(response, access_token, refresh_token):
    """Seta os cookies HttpOnly de autenticação na resposta."""
    secure = getattr(settings, 'JWT_COOKIE_SECURE', False)
    samesite = getattr(settings, 'JWT_COOKIE_SAMESITE', 'Lax')

    # Cookie do access token: 15 minutos
    response.set_cookie(
        key='access',
        value=access_token,
        max_age=15 * 60,          # 15 minutos em segundos
        httponly=True,             # JavaScript NÃO pode ler
        secure=secure,             # Apenas HTTPS em produção
        samesite=samesite,
        path='/',
    )

    # Cookie do refresh token: 7 dias
    response.set_cookie(
        key='refresh',
        value=refresh_token,
        max_age=7 * 24 * 60 * 60,  # 7 dias em segundos
        httponly=True,
        secure=secure,
        samesite=samesite,
        path='/',
    )


class CustomTokenObtainPairView(APIView):
    serializer_class = EmailTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        access_token = data.pop('_access_token')
        refresh_token = data.pop('_refresh_token')

        # Monta resposta com dados de perfil (sem tokens no body)
        response = Response(data, status=status.HTTP_200_OK)

        # Seta tokens como cookies HttpOnly — JavaScript não consegue ler
        _set_auth_cookies(response, access_token, refresh_token)

        return response


class MeView(APIView):
    """
    GET /me/ — Retorna os dados do usuário autenticado (via cookie HttpOnly).
    Usado pelo AuthContext para verificar se a sessão ainda é válida ao recarregar a página.
    """
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            cliente = user.cliente
            return Response({
                'id': cliente.id,
                'nome': cliente.nome,
                'email': user.email,
                'perfil': cliente.perfil,
                'has_password': user.has_usable_password(),
            })
        except Exception:
            return Response({
                'id': None,
                'nome': user.username,
                'email': user.email,
                'perfil': 'user',
                'has_password': user.has_usable_password(),
            })
