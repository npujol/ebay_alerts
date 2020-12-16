from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, EmailMessage
from ebay_alerts.settings import EMAIL_HOST_USER
from django.urls import reverse
from .models import Alert


def send_email_to_delete_a_alert(email, uuid=None):
    alert = get_object_or_404(Alert, uuid=uuid)
    link = reverse("alerts:alert-detail")
    message = f"""\
    If do you want to delete the alert:
    Search:{alert.search_term} \
    Interval of time: {alert.interval_time}.\
    You must to click in the follow link: {link}. """

    send_mail(
        "Alert delete",
        message,
        EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return f"The email to the user {email} was sended"


def send_email_after_create(email, uuid=None):
    alert = get_object_or_404(Alert, uuid=uuid)
    message = f"""
    You had created a new alert:
    Search:{alert.search_term} 
    Interval of time: {alert.interval_time}."""

    send_mail(
        "New alert was created.",
        message,
        EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return f"The email to the user {email} was sended"


def send_email_with_ebay_answer(email):
    send_mail(
        "Subject here",
        "Here is the message.",
        EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return f"The email to the user {email} was sended"