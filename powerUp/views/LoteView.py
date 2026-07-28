from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from powerUp.models import Lote
from powerUp.serializers.LoteSerializer import LoteSerializer
from powerUp.permissions import IsPerfilAdmin

class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all().order_by('-data_entrada', '-id') 
    serializer_class = LoteSerializer
    permission_classes = [IsPerfilAdmin]

    # Configurações de filtro
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['produto'] 
    ordering_fields = ['validade', 'quantidade', 'data_entrada'] 
    search_fields = ['produto__nome'] 

    @action(detail=False, methods=['post'], url_path='bulk_delete')
    def bulk_delete(self, request):
        ids = request.data.get('ids', [])
        if not ids or not isinstance(ids, list):
            return Response(
                {"detail": "Informe uma lista de IDs válida."},
                status=status.HTTP_400_BAD_REQUEST
            )
        deleted_count, _ = Lote.objects.filter(id__in=ids).delete()
        return Response(
            {"detail": f"{deleted_count} lote(s) excluído(s) com sucesso."},
            status=status.HTTP_200_OK
        )