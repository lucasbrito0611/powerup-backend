# Usa uma imagem oficial leve do Python
FROM python:3.11-slim

# Define variáveis de ambiente para o Python não gerar arquivos .pyc e não reter saídas em buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala as dependências do sistema necessárias para compilar pacotes ou conectar ao banco
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o arquivo de requisitos primeiro (otimiza o cache do Docker)
COPY requirements.txt /app/

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do código do projeto para o container
COPY . /app/

# Expõe a porta padrão do Django REST
EXPOSE 8000

# Comando padrão para rodar o servidor de desenvolvimento
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]