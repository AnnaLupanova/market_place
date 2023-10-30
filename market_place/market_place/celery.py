import os
from celery import Celery, shared_task
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_place.settings')
app = Celery('market_place')
app.config_from_object('django.conf:settings', namespace='CELERY')

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




#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, task_one.s, name='add every 10')
#     #
#     # # Calls test('world') every 30 seconds
#     # sender.add_periodic_task(30.0, test.s('world'), expires=10)
#     #
#     # # Executes every Monday morning at 7:30 a.m.
#     # sender.add_periodic_task(
#     #     crontab(hour=7, minute=30, day_of_week=1),
#     #     test.s('Happy Mondays!'),
#     # )



