from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError) and response is not None:
        custom_errors = []

        # 1. CASO DJOSER (Lista)
        if isinstance(response.data, list):
            for message in response.data:
                custom_errors.append(f"{message}")

        # 2. CASO PADRÃO (Dicionário)
        elif isinstance(response.data, dict):
            for field, messages in response.data.items():
                if isinstance(messages, list):
                    for message in messages:
                        if field == "non_field_errors":
                            custom_errors.append(f"{message}")
                        else:
                            custom_errors.append(f"{message}") 
                else:
                    custom_errors.append(f"{field.capitalize()}: {messages}")

        return Response(
            {
                "detail": "Erro de validação",
                "errors": custom_errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    return response


# --- VALIDAÇÃO DE UPLOAD SEGURO (Devoluções) ---
import filetype

ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf']
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB

def validar_arquivo_devolucao(arquivo):
    if not arquivo:
        return
    
    if arquivo.size > MAX_UPLOAD_SIZE:
        raise ValidationError("Arquivo muito grande. Máximo 5MB.")
        
    try:
        # Lê os primeiros 2048 bytes para analisar a assinatura binária
        kind = filetype.guess(arquivo.read(2048))
        arquivo.seek(0)
        
        if kind is None or kind.mime not in ALLOWED_MIME_TYPES:
            raise ValidationError("Tipo de arquivo não permitido ou corrompido.")
    except Exception as e:
        if isinstance(e, ValidationError):
            raise e
        raise ValidationError("Erro ao validar o formato do arquivo.")