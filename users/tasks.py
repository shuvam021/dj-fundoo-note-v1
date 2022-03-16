from __future__ import absolute_import

import time

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
# from django.urls import reverse
from config.celery import app as celery_app


# @celery_app.task()
@shared_task
def send_verify_email_task(email):
    subject = "Tasks Check"
    body = f"Hii {email.split('2')[0]}\n"
    try:
        time.sleep(2)
        send_mail(subject, body, settings.EMAIL_HOST, [email])
        return 'mail send'
    except Exception as e:
        print(e)
