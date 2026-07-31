from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from powerUp.models import SolicitacaoDevolucao
from powerUp.permissions import IsPerfilAdmin
from powerUp.serializers.DevolucaoSerializer import SolicitacaoDevolucaoSerializer


class DevolucaoViewSet(viewsets.ModelViewSet):
    serializer_class = SolicitacaoDevolucaoSerializer
    permission_classes = [IsAuthenticated]

    # Campos suportados pela busca, ordenação e filtro (usados pelo data-provider do Refine)
    search_fields = ['user__cliente__nome', 'motivo']
    ordering_fields = ['id', 'status', 'data_solicitacao', 'total']
    ordering = ['-data_solicitacao']
    filterset_fields = ['status']

    # ─── Permissões por ação ──────────────────────────────────────────────────
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsPerfilAdmin()]
        return [IsAuthenticated()]

    # ─── Queryset com isolamento por perfil ──────────────────────────────────
    def get_queryset(self):
        user = self.request.user

        is_admin = (
            hasattr(user, 'cliente') and user.cliente.perfil == 'admin'
        )

        if is_admin:
            return (
                SolicitacaoDevolucao.objects
                .select_related('user__cliente', 'pedido')
                .prefetch_related('itens__pedido_item__produto')
                .order_by('-data_solicitacao')
            )

        # Usuário comum: escopo estrito — só vê as suas devoluções
        return (
            SolicitacaoDevolucao.objects
            .filter(user=user)
            .select_related('user__cliente', 'pedido')
            .prefetch_related('itens__pedido_item__produto')
            .order_by('-data_solicitacao')
        )

    # ─── Validação extra na edição ────────────────────────────────────────────
    def update(self, request, *args, **kwargs):
        allowed_fields = {'status'}
        received_fields = set(request.data.keys())
        disallowed = received_fields - allowed_fields

        if disallowed:
            return Response(
                {"erro": f"Campos não permitidos: {', '.join(disallowed)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().update(request, *args, **kwargs)

    # ─── Criação: vincula ao usuário autenticado ──────────────────────────────
    def perform_create(self, serializer):
        """Garante que a solicitação seja sempre vinculada ao usuário logado."""
        serializer.save(user=self.request.user)

    # ─── Ação: cancelar (exclusiva do dono) ──────────────────────────────────
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        solicitacao = self.get_object()

        # Segurança: verifica se o objeto pertence ao usuário logado
        if solicitacao.user != request.user:
            return Response(
                {"erro": "Você não tem permissão para cancelar esta solicitação."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if solicitacao.status != '1':
            return Response(
                {"erro": "Esta solicitação não pode mais ser cancelada."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        solicitacao.status = '5'
        solicitacao.save()

        serializer = self.get_serializer(solicitacao)
        return Response(serializer.data, status=status.HTTP_200_OK)