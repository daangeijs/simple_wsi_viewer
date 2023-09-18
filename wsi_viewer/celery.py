import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wsi_viewer.settings')

app = Celery('wsi_viewer')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# # run celery eager
# app.conf.update(
#     task_always_eager=True,
# )
