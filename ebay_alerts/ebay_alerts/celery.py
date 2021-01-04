import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ebay_alerts.settings")
app = Celery("ebay_alerts")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
