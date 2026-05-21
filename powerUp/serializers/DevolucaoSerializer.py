from rest_framework import serializers
from powerUp.models import SolicitacaoDevolucao, ItemDevolvido, PedidoItem
from powerUp.utils import validar_arquivo_devolucao

class ItemDevolvidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDevolvido
        fields = ['id', 'pedido_item', 'quantidade']


class SolicitacaoDevolucaoSerializer(serializers.ModelSerializer):
    def validate_arquivo(self, value):
        validar_arquivo_devolucao(value)
        return value

    itens = ItemDevolvidoSerializer(many=True, read_only=True)
    
    pedido_id = serializers.IntegerField(source='pedido.id', read_only=True)
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = SolicitacaoDevolucao
        
        fields = ['id', 'pedido_id', 'status', 'status_display', 'motivo', 'arquivo', 'data_solicitacao', 'itens', 'total']
        read_only_fields = ['id',  'pedido_id',  'status',  'status_display',  'data_solicitacao',  'itens']