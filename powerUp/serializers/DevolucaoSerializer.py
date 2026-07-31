from rest_framework import serializers
from powerUp.models import SolicitacaoDevolucao, ItemDevolvido, PedidoItem
from powerUp.utils import validar_arquivo_devolucao

class ItemDevolvidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='pedido_item.produto.nome', read_only=True)

    class Meta:
        model = ItemDevolvido
        fields = ['id', 'pedido_item', 'produto_nome', 'quantidade']


class SolicitacaoDevolucaoSerializer(serializers.ModelSerializer):
    def validate_arquivo(self, value):
        validar_arquivo_devolucao(value)
        return value

    itens = ItemDevolvidoSerializer(many=True, read_only=True)
    
    pedido_id = serializers.IntegerField(source='pedido.id', read_only=True)
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    # Campo adicional para exibição do nome do cliente no painel admin
    user_nome = serializers.SerializerMethodField(read_only=True)

    def get_user_nome(self, obj):
        try:
            return obj.user.cliente.nome
        except AttributeError:
            return obj.user.get_full_name() or obj.user.username

    class Meta:
        model = SolicitacaoDevolucao
        
        fields = ['id', 'pedido_id', 'user_nome', 'status', 'status_display', 'motivo', 'arquivo', 'data_solicitacao', 'itens', 'total']
        # 'status' removido de read_only_fields para permitir atualização pelo admin via PATCH
        read_only_fields = ['id', 'pedido_id', 'user_nome', 'status_display', 'data_solicitacao', 'itens']