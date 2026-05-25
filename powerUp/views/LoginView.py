from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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

        return {
            'refresh': str(refresh),
            'access': access,
            'id': cliente_id,
            'nome': nome,
            'email': user.email,
            'perfil': perfil,
        }

class CustomTokenObtainPairView(APIView):
    serializer_class = EmailTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

