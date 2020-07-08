import logging
import os
import sentry_sdk

from celery import Celery
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.conf import settings


# Sentry
if settings.IS_PROD:
    sentry_logging = LoggingIntegration(level=settings.SENTRY_LOG_LEVEL, event_level=logging.ERROR)
    sentry_sdk.init(dsn=settings.SENTRY_DSN, integrations=[sentry_logging, DjangoIntegration(), CeleryIntegration()])


app = Celery('{{ cookiecutter.project_slug }}')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
