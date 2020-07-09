import os
{%- if cookiecutter.use_sentry == 'y' %}
import sentry_sdk
import logging
{%- endif %}

from pathlib import Path
{%- if cookiecutter.use_sentry == 'y' %}
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
{%- endif %}

ROOT_DIR = Path(__file__).parent.parent
APPS_DIR = ROOT_DIR / 'apps'
APIS_DIR = ROOT_DIR / 'apis'


# GENERAL
DEPLOYMENT_ENVIRONMENT = os.getenv('DEPLOYMENT_ENVIRONMENT', 'PROD')
IS_PROD = True if DEPLOYMENT_ENVIRONMENT == 'PROD' else False
IS_DEV = True if DEPLOYMENT_ENVIRONMENT == 'DEV' else False
IS_TEST = True if DEPLOYMENT_ENVIRONMENT == 'TEST' else False

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False if IS_PROD else True
# https://docs.djangoproject.com/en/ref/settings/#secret-key
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [v.strip() for v in os.getenv('DJANGO_ALLOWED_HOSTS').strip().split(',') if v]
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = 'Europe/Moscow'
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'ru-ru'
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = False
# https://docs.djangoproject.com/en/2.2/ref/settings/#append-slash
APPEND_SLASH = True
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'config.urls'
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# DATABASES
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': os.getenv('POSTGRES_ENGINE', 'django.db.backends.postgresql_psycopg2'),
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': int(os.getenv('POSTGRES_PORT', 5432)),
        'CONN_MAX_AGE': int(os.getenv('POSTGRES_CONN_MAX_AGE', 60)),
        'ATOMIC_REQUESTS': bool(os.getenv('POSTGRES_ATOMIC_REQUESTS', True)),
    },
}

# APPS
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
{%- if cookiecutter.use_drf == 'y' %}

    'rest_framework',
    'rest_framework.authtoken',
{%- endif %}
{%- if cookiecutter.use_corsheaders == 'y' %}
    'corsheaders',
{%- endif %}
{%- if cookiecutter.use_drf_yasg == 'y' %}
    'drf_yasg',
{%- endif %}
{%- if cookiecutter.use_celery == 'y' %}
    'django_celery_beat',
{%- endif %}
]

# AUTHENTICATION
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

# PASSWORDS
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# MIDDLEWARE
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    {%- if cookiecutter.use_corsheaders == 'y' %}
    'corsheaders.middleware.CorsMiddleware',
    {%- endif %}
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# SECURITY
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = 'DENY'
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = bool(os.getenv('DJANGO_SECURE_SSL_REDIRECT', False))
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = bool(os.getenv('DJANGO_SESSION_COOKIE_SECURE', False))
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = bool(os.getenv('DJANGO_CSRF_COOKIE_SECURE', False))
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = bool(os.getenv('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', False))
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = bool(os.getenv('DJANGO_SECURE_HSTS_PRELOAD', False))
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = bool(os.getenv('DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', False))

if IS_PROD:
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
    # TODO: set this to 60 seconds first and then to 518400 once you prove the former works
    SECURE_HSTS_SECONDS = 60

# EMAIL
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = os.getenv('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
# https://docs.djangoproject.com/en/2.2/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = os.getenv('DJANGO_DEFAULT_FROM_EMAIL', '{{ cookiecutter.project_slug }}@example.com')
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = os.getenv('DJANGO_SERVER_EMAIL', DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = os.getenv('DJANGO_EMAIL_SUBJECT_PREFIX', '{{ cookiecutter.project_slug }} ')

# TEMPLATES
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [str(ROOT_DIR / 'templates')],
        'OPTIONS': {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

# STATIC
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR / 'staticfiles')
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(ROOT_DIR / 'static')]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# MEDIA
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(ROOT_DIR / 'media')
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# FIXTURES
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(ROOT_DIR / 'fixtures'),)

{%- if cookiecutter.use_drf == 'y' %}

# DRF
# https://www.django-rest-framework.org/api-guide/settings/#settings
REST_FRAMEWORK = {
    #'EXCEPTION_HANDLER': 'apps.core.services.drf.custom_exception_handler',
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_INPUT_FORMATS': ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S'],
}
{%- endif %}
{%- if cookiecutter.use_celery == 'y' %}

# Celery
if USE_TZ:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ['json']
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = 'json'
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = 'json'
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 120
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
{%- endif %}
{%- if cookiecutter.use_sentry == 'y' %}

# Sentry
SENTRY_DSN = os.getenv('SENTRY_DSN')
SENTRY_LOG_LEVEL = int(os.getenv('DJANGO_SENTRY_LOG_LEVEL', logging.INFO))
if IS_PROD:
    sentry_logging = LoggingIntegration(level=SENTRY_LOG_LEVEL, event_level=logging.ERROR)
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[sentry_logging, DjangoIntegration(), CeleryIntegration()])
{%- endif %}
{%- if cookiecutter.use_redis == 'y' %}

# Cache redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://redis:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # Mimicing memcache behavior.
            # http://jazzband.github.io/django-redis/latest/#_memcached_exceptions_behavior
            'IGNORE_EXCEPTIONS': True,
        },
    }
}
{%- endif %}

if not DEBUG:
    # Django logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'}
        },
        'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}},
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler',
            },
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
        },
        'root': {'level': 'INFO', 'handlers': ['console']},
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'INFO',
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry_sdk': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False
            },
            'django.security.DisallowedHost': {
                'level': 'ERROR',
                'handlers': ['null'],
                'propagate': False,
            },
        },
    }

{%- if cookiecutter.use_corsheaders == 'y' %}

# Django cors headers
if IS_PROD:
    # https://github.com/adamchainz/django-cors-headers#cors_origin_whitelist
    CORS_ORIGIN_WHITELIST = []
else:
    # https://github.com/adamchainz/django-cors-headers#cors_origin_regex_whitelist
    CORS_ORIGIN_REGEX_WHITELIST = [r'^http[s]*:\/\/[\d\w.-]+:[\d]+$']
{%- endif %}
{%- if cookiecutter.use_drf_yasg == 'y' %}

# Swagger Settings
# https://drf-yasg.readthedocs.io/en/stable/security.html#security-definitions
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        }
    }
}
{%- endif %}

# Your stuff...

