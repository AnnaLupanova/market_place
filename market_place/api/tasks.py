from celery import shared_task
from .models import Provider, Product
from market_place.celery import app
import random

@app.task
def increment_debt():
    providers = Provider.objects.filter(parent__isnull=False)
    for provider in providers:
        provider.debt_to_provider += random.randrange(5, 501)
    bulk_msj = Provider.objects.bulk_update(providers, ['debt_to_provider'])
    return


@app.task
def decrement_debt():
    providers = Provider.objects.filter(parent__isnull=False)
    for provider in providers:
        provider.debt_to_provider -= random.randrange(100, 10000)
    bulk_msj = Provider.objects.bulk_update(providers, ['debt_to_provider'])
    return