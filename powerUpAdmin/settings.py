from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', 
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken', 
    'djoser',
    'anymail', 
    'django_filters',
    'axes',
    'powerUp',
    'rest_framework_simplejwt.token_blacklist',
]

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'powerUp.utils.custom_exception_handler',
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "powerUp.authentication.JWTCookieAuthentication",
    ],
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'recuperar/{uid}/{token}',
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'SEND_ACTIVATION_EMAIL': False,
    'SEND_CONFIRMATION_EMAIL': False,
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'DOMAIN': 'localhost:3000', 
    'SITE_NAME': 'PowerUp',
}

# --- CONFIGURAÇÃO DE E-MAIL (RESEND) ---

EMAIL_BACKEND = "anymail.backends.resend.EmailBackend"

ANYMAIL = {
    "RESEND_API_KEY": os.getenv("RESEND_API_KEY"),
}

DEFAULT_FROM_EMAIL = "onboarding@resend.dev"


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000'
).split(',')

# Necessário para que o navegador envie cookies em requisições cross-origin
CORS_ALLOW_CREDENTIALS = True

# Headers permitidos nas requisições cross-origin (inclui padrões do DRF + cookie)
CORS_ALLOW_HEADERS = [
    'accept',
    'authorization',
    'content-type',
    'origin',
    'x-csrftoken',
    'x-requested-with',
]

# --- CONFIGURAÇÃO JWT ---
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Cookie HttpOnly — secure=True apenas em produção (HTTPS)
JWT_COOKIE_SECURE = not DEBUG   # False em dev, True em prod
JWT_COOKIE_SAMESITE = 'Lax'    # Lax funciona em localhost; Strict requer mesma origem

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# --- CONFIGURAÇÃO DO DJANGO-AXES (Rate Limiting) ---
AXES_FAILURE_LIMIT = 5            # Bloqueia após 5 falhas consecutivas
AXES_COOLOFF_TIME = 1             # Tempo de bloqueio (1 hora)
AXES_LOCKOUT_PARAMETERS = ['ip_address', 'username']  # Bloqueia baseado em IP e username
AXES_RESET_ON_SUCCESS = True      # Reseta as falhas em caso de sucesso

ROOT_URLCONF = 'powerUpAdmin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'powerUpAdmin.wsgi.application'


# Usa PostgreSQL se as variáveis de ambiente estiverem definidas (Docker), senão usa SQLite (dev local)
if os.getenv('DB_ENGINE'):
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
            'NAME': os.getenv('DB_NAME', 'powerup'),
            'USER': os.getenv('DB_USER', 'powerup_user'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'powerup_pass'),
            'HOST': os.getenv('DB_HOST', 'db'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'

MEDIA_URL='/media/'
MEDIA_ROOT= os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1