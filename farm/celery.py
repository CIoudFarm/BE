# farm/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "farm.settings")
app = Celery("farm")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
