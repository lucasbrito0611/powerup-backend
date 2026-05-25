# ⚡ PowerUP — Backend

Plataforma de e-commerce completa para suplementos e produtos fitness. API REST construída com **Django REST Framework**, autenticação via **JWT em HttpOnly Cookies**, banco de dados **PostgreSQL** e pronta para rodar em Docker.

---

## ✨ Destaques

- 🔐 **Autenticação segura** com JWT armazenado em cookie HttpOnly (sem exposição no `localStorage`)
- 🔄 **Refresh automático** de token via endpoint dedicado
- 🛡️ **Proteção contra força bruta** com `django-axes` (bloqueio por IP + username)
- 🛒 **Carrinho persistente** com migração do carrinho anônimo ao logar
- 📦 **Gestão completa de pedidos**, devoluções e notificações
- 💌 **E-mails transacionais** com Resend (recuperação de senha)
- 🐳 **Docker Compose** com PostgreSQL, Backend e Frontend orquestrados

---

## 🧭 Visão Geral da Stack

| Camada         | Tecnologia                                  |
| -------------- | ------------------------------------------- |
| **Backend**    | Python 3 · Django 4 · Django REST Framework |
| **Auth**       | SimpleJWT · JWT em HttpOnly Cookie          |
| **Banco**      | PostgreSQL 16 (Docker) · SQLite (dev local) |
| **E-mail**     | Resend via django-anymail                   |
| **Rate Limit** | django-axes                                 |
| **CORS**       | django-cors-headers                         |
| **Frontend**   | Next.js 15 (repositório separado)           |

---

## 📂 Estrutura do Projeto

```
powerup-backend/
├── powerUp/
│   ├── models/
│   │   ├── Produto.py          # Produto e atributos
│   │   ├── Cliente.py          # Perfil de usuário
│   │   ├── Carrinho.py         # Itens do carrinho
│   │   ├── Pedido.py           # Pedidos e itens de pedido
│   │   ├── Devolucao.py        # Solicitações de devolução
│   │   ├── Favorito.py         # Lista de favoritos
│   │   ├── Endereco.py         # Endereços do cliente
│   │   ├── Cartao.py           # Cartões salvos
│   │   ├── Lote.py             # Estoque por lote
│   │   ├── Notificacao.py      # Notificações do usuário
│   │   └── AvaliacaoProduto.py # Avaliações de produtos
│   ├── views/
│   │   ├── LoginView.py        # Login + endpoint /me
│   │   ├── LogoutView.py       # Logout com limpeza de cookie
│   │   ├── RefreshCookieView.py# Refresh de token via cookie
│   │   ├── ProdutoView.py      # CRUD de produtos
│   │   ├── ClienteView.py      # CRUD de clientes
│   │   ├── CarrinhoView.py     # Carrinho + migração anônima
│   │   ├── PedidoView.py       # Pedidos e checkout
│   │   ├── DevolucaoView.py    # Devoluções
│   │   ├── FavoritoView.py     # Favoritos
│   │   ├── EnderecoView.py     # Endereços
│   │   ├── CartaoView.py       # Cartões
│   │   ├── NotificacaoView.py  # Notificações
│   │   ├── LoteView.py         # Lotes de estoque
│   │   ├── LoteAlertaView.py   # Alertas de estoque baixo
│   │   ├── PromocoesView.py    # Promoções
│   │   └── RedefinirSenhaView.py # Redefinição de senha
│   ├── authentication.py       # Autenticação JWT via cookie
│   ├── permissions.py          # Permissões customizadas
│   ├── serializers/            # Serializers DRF
│   ├── signals.py              # Signals (ex: criação de perfil)
│   └── utils.py                # Utilitários e exception handler
├── powerUpAdmin/
│   ├── settings.py             # Configurações Django
│   └── urls.py                 # Roteamento principal
├── docker-compose.yml          # Orquestração Docker
├── Dockerfile
├── requirements.txt
├── manage.py
└── .env.example
```

---

## 🔌 Endpoints da API

### Autenticação

| Método | Endpoint            | Descrição                                |
| ------ | ------------------- | ---------------------------------------- |
| `POST` | `/login/`           | Login — retorna JWT em cookie HttpOnly   |
| `POST` | `/logout/`          | Logout — limpa o cookie de autenticação  |
| `POST` | `/refresh/`         | Renova o access token via refresh cookie |
| `GET`  | `/me/`              | Retorna dados do usuário autenticado     |
| `POST` | `/redefinir-senha/` | Solicita redefinição de senha por e-mail |
| `POST` | `/auth/users/`      | Cadastro de novo usuário (Djoser)        |

### Recursos

| Método            | Endpoint              | Descrição                       |
| ----------------- | --------------------- | ------------------------------- |
| `GET`             | `/produtos/`          | Listagem de produtos            |
| `GET`             | `/produtos/{id}/`     | Detalhe do produto              |
| `GET/POST`        | `/pedidos/`           | Listagem e criação de pedidos   |
| `GET/POST/DELETE` | `/carrinho/`          | Gerenciamento do carrinho       |
| `POST`            | `/carrinho/migracao/` | Migração do carrinho anônimo    |
| `GET/POST`        | `/favoritos/`         | Lista de favoritos              |
| `GET/POST`        | `/enderecos/`         | Endereços do cliente            |
| `GET/POST`        | `/cartoes/`           | Cartões salvos                  |
| `GET/POST`        | `/devolucoes/`        | Solicitações de devolução       |
| `GET`             | `/notificacoes/`      | Notificações do usuário         |
| `GET`             | `/promocoes/`         | Produtos em promoção            |
| `GET`             | `/lotes/`             | Lotes de estoque                |
| `GET`             | `/lote/alerta/`       | Alerta de estoque baixo (admin) |

---

## ✅ Requisitos

- **Python 3.9+** e **pip**
- Repositório do **frontend** clonado na mesma pasta pai (necessário apenas para rodar via Docker Compose)

> **Docker e Docker Compose** são opcionais — necessários apenas se quiser subir toda a stack (banco + backend + frontend) de forma orquestrada.

---

## 🛠️ Configuração Inicial

### 1. Estrutura de Pastas

Os repositórios do backend e frontend **precisam estar lado a lado** na mesma pasta, pois o `docker-compose.yml` referencia o frontend com caminho relativo (`../powerup-frontend`).

```bash
# Crie a pasta raiz do projeto
mkdir PowerUP && cd PowerUP

# Clone os dois repositórios
git clone https://github.com/lucasbrito0611/powerup-backend.git
git clone https://github.com/lucasbrito0611/powerup-frontend.git
```

### 2. Variáveis de Ambiente

Entre na pasta do backend e crie o arquivo `.env`:

```bash
cd powerup-backend
cp .env.example .env
# No Windows (CMD): copy .env.example .env
```

Edite o arquivo `.env` com seus dados:

```env
# Chave secreta do Django — gere uma com:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# ⚠️ Se o valor contiver "$", duplique como "$$" para o Docker não interpretar como variável.
SECRET_KEY=django-insecure-troque-esta-chave-em-producao

# Modo debug — use True apenas em desenvolvimento
DEBUG=True

# Hosts permitidos (separados por vírgula)
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,backend

# CORS — origens permitidas para o frontend
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Banco de dados (PostgreSQL via Docker)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=powerup
DB_USER=powerup_user
DB_PASSWORD=powerup_pass
DB_HOST=db
DB_PORT=5432

# E-mail transacional via Resend (https://resend.com)
RESEND_API_KEY=re_sua_chave_aqui
```

### 3. Subindo o Projeto

Ainda dentro de `powerup-backend`, execute:

```bash
docker compose up --build
```

O Docker Compose irá automaticamente:

1. 🐘 Subir o banco **PostgreSQL 16**
2. ⚙️ Executar as **migrations** do Django
3. 🚀 Iniciar a **API** na porta `8000`
4. 🌐 Iniciar o **Frontend** (Next.js) na porta `3000`

| Serviço  | URL                         |
| -------- | --------------------------- |
| API      | http://localhost:8000       |
| Frontend | http://localhost:3000       |
| Admin    | http://localhost:8000/admin |

---

## 📦 Importando Dados de Exemplo (Opcional)

Para popular o banco com dados de teste, coloque o arquivo `dados_migrate.json` na raiz do repositório e execute:

```bash
# Com os containers em execução, em um novo terminal:
docker exec django_backend python manage.py loaddata /app/dados_migrate.json
```

---

## 💻 Desenvolvimento Local (Sem Docker)

Para rodar apenas o backend localmente com SQLite:

```bash
# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# Instale as dependências
pip install -r requirements.txt

# Rode as migrations
python manage.py migrate

# Inicie o servidor
python manage.py runserver
```

> ⚠️ Sem Docker, o projeto usa **SQLite** automaticamente. Para usar PostgreSQL, configure as variáveis `DB_*` no seu `.env`.

---

## 🔐 Segurança

| Recurso                     | Implementação                              |
| --------------------------- | ------------------------------------------ |
| JWT em HttpOnly Cookie      | Tokens não acessíveis via JavaScript       |
| Refresh automático          | `RefreshCookieView` com rotação de tokens  |
| Blacklist de tokens         | `rest_framework_simplejwt.token_blacklist` |
| Proteção contra brute force | `django-axes` — bloqueio por IP + username |
| CORS configurado            | `django-cors-headers` com credenciais      |
