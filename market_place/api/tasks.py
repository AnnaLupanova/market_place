from celery import shared_task
from .models import Provider, Product
from market_place.celery import app
import random
from django.core.mail import EmailMessage, send_mail
import time
import base64
from django.template.loader import render_to_string

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

@shared_task(serializer='json', name="send_mail")
def send_email_fun(subject, message, sender, receiver):
    ctx = {
        'qr_code_image': message,
    }
    message_ = render_to_string('api/qrcode.html', ctx)
    mail = EmailMessage(subject=subject, body=message_, from_email=sender, to=[receiver])
    mail.content_subtype = 'html'
    mail.send()