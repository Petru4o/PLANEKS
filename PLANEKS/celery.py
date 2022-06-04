from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PLANEKS.settings')

app = Celery('PLANEKS')
app.config_from_object('django.conf:settings', namespace='CELERY')
CAR_BROKER_URL = 'redis://localhost:6379'

app.autodiscover_tasks(settings.INSTALLED_APPS)