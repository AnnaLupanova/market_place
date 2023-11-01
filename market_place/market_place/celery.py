import os
from celery import Celery, shared_task
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_place.settings')
app = Celery('market_place', broker='redis://redis:6379', backend='redis://redis:6379')
app.conf.broker_url = 'redis://redis:6379/0'

app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'increment-debt': {
        'task': 'api.tasks.increment_debt',
        'schedule': crontab(minute=0, hour='*/3')
    },
    'decrement-debt': {
        'task': 'api.tasks.decrement_debt',
        'schedule': crontab(hour=6, minute=30, day_of_week=0)
    }

}



