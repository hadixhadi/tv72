import os
from celery import Celery
from celery.schedules import schedule, crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.envs.develop')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
CELERY_TIMEZONE = "Asia/Tehran"
app.conf.broker_url = 'amqp://rabbitmq'
CELERY_RESULT_BACKEND = 'django-db'



