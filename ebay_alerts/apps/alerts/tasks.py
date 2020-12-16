from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.urls import reverse
from .models import Alert


@shared_task(name="Send Ebay search results")
def send_creation_email(email):
    message = """
    You had created a new alert:
    Search: 
    Interval of time:."""

    send_mail(
        "New alert was created.",
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return f"The email to the user {email} was sended"
