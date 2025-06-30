import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
if env_path.exists():
    load_dotenv(env_path)

# docker, local
ENV_TYPE = os.environ.get('ENV_TYPE', 'docker')


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-gang-bang7')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_pgschemas',
    'ninja',
    'tenants',
    'contacts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'tenants.middleware.TenantMiddleware',  # Возвращаем кастомный middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'


DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgres://postgres:postgres@localhost:5432/contacts_crm'
)
db_parts = DATABASE_URL.split('/')
db_name = db_parts[-1]

host_string = DATABASE_URL.split('@')[-1].split('/')[0]
if ':' in host_string:
    host, port = host_string.split(':')
else:
    host, port = host_string, '5432'

if ENV_TYPE == 'local':
    host = 'localhost'

auth_part = DATABASE_URL.split('/')[2].split('@')[0]
if ':' in auth_part:
    user, password = auth_part.split(':')
else:
    user, password = 'postgres', 'postgres'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_name,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
    }
}

DATABASE_ROUTERS = ['django_pgschemas.routers.TenantAppsRouter']

TENANT_MODEL = 'tenants.Tenant'
DOMAIN_MODEL = 'tenants.Domain'
TENANT_SCHEMA_PREFIX = os.environ.get('TENANT_SCHEMA_PREFIX', 'contact_')

TENANTS = {
    # Public (shared) схема
    'public': {
        'SCHEMA_NAME': 'public',  # явно указываем имя схемы
        'APPS': [
            # Общесистемные компоненты
            'django.contrib.admin',  # админка
            'django.contrib.auth',  # базовая авторизация
            'django.contrib.contenttypes',  # модели контент-типов
            'django.contrib.sessions',  # сессии
            'django.contrib.messages',
            'django.contrib.staticfiles',  # статика
            'django_pgschemas',  # менеджер схем
            'tenants',  # модели тенантов
        ],
    },
    # Настройка для всех динамических арендаторов
    'default': {
        'TENANT_MODEL': 'tenants.Tenant',
        'DOMAIN_MODEL': 'tenants.Domain',
        'APPS': [
            # 'django.contrib.admin',
            # "django.contrib.auth",
            # "django.contrib.sessions",
            # 'django.contrib.sites',
            'ninja',
            'contacts',
        ],
        'URLCONF': 'app.urls',
    },
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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# celery
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
