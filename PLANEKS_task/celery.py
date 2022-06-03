from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PLANEKS_task.settings')

app = Celery('fakedata')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()
