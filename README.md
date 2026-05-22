# PowerUP - Backend

Este é o backend do projeto PowerUP, construído com Django REST Framework. O projeto utiliza PostgreSQL como banco de dados principal no ambiente Docker e SQLite para desenvolvimento local sem Docker.

## 🚀 Requisitos

- [Docker](https://www.docker.com/) e Docker Compose instalados na máquina.
- Repositório do frontend clonado lado a lado com este repositório (obrigatório para rodar via Docker Compose).

## 🛠️ Configuração Inicial

Para rodar o projeto completo (Frontend, Backend e Banco de Dados) via Docker, siga os passos abaixo:

### 1. Estrutura de Pastas

É **obrigatório** que os repositórios do backend e frontend estejam na mesma pasta pai, pois o `docker-compose.yml` faz referência ao frontend utilizando caminho relativo (`../powerup-frontend`).

```bash
# Crie uma pasta raiz para o projeto
mkdir PowerUP && cd PowerUP

# Clone os dois repositórios
git clone https://github.com/lucasbrito0611/powerup-backend.git
git clone https://github.com/lucasbrito0611/powerup-frontend.git
```

### 2. Variáveis de Ambiente

Entre na pasta do backend e crie o arquivo de configuração de ambiente:

```bash
cd powerup-backend
cp .env.example .env  # No Windows (CMD), use: copy .env.example .env
```

Edite o arquivo `.env` gerado e preencha com seus dados reais:
- `SECRET_KEY`: Chave secreta do Django (não use o valor padrão em produção). Lembre-se de duplicar o sinal de dólar (`$$`) caso sua chave possua um `$`, para que o Docker não interprete como variável.
- `RESEND_API_KEY`: Sua chave do Resend para envio de e-mails.

### 3. Rodando o Projeto

Ainda dentro da pasta `powerup-backend`, execute:

```bash
docker compose up --build
```

O Docker Compose irá:
1. Subir o banco PostgreSQL.
2. Rodar as migrations do Django.
3. Subir a API do Backend na porta `8000`.
4. Subir o Frontend (Next.js) na porta `3000`.

Acesse a API em: `http://localhost:8000`

## 📦 Importando Dados de Exemplo (Opcional)

Se você tiver um arquivo de dump do banco (ex: `dados_migrate.json`) e quiser popular o PostgreSQL com ele, coloque o arquivo na raiz da pasta `powerup-backend` (que é espelhada para dentro do container) e rode o comando abaixo em um novo terminal:

```bash
# Executar enquanto os containers estiverem rodando
docker exec django_backend python manage.py loaddata /app/dados_migrate.json
```

## 💻 Desenvolvimento Local (Sem Docker)

Se preferir rodar apenas o backend localmente sem o Docker (utilizará o SQLite local):

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
