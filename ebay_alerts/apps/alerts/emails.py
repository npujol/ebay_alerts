from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import HttpRequest
from django.template.loader import get_template
from .models import Alert
from .fake_ebay import get_filtered_data
from django.urls import reverse
from .utils import get_relative_url


def send_email_after_create(uuid=None):
    alert = get_object_or_404(Alert, uuid=uuid)
    email = alert.owner.email
    subject, from_email, to = (
        "A new alert was created.",
        settings.EMAIL_HOST_USER,
        email,
    )

    text_content = get_template("create_email.txt").render({"alert": alert})
    html_content = get_template("create_email.html").render({"alert": alert})
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send(
        fail_silently=False,
    )
    return f"The task: send_email_after_create to the user {email} was started"


def send_email_to_delete(uuid=None):
    alert = get_object_or_404(Alert, uuid=uuid)
    email = alert.owner.email
    subject, from_email, to = (
        "Delete an alert.",
        settings.EMAIL_HOST_USER,
        email,
    )
    link = HttpRequest.build_absolute_uri(
        reverse("alerts:alert-detail", kwargs={"uuid": alert.uuid}),
    )
    text_content = get_template("delete_email.txt").render(
        {"alert": alert, "link": link}
    )
    html_content = get_template("delete_email.html").render(
        {"alert": alert, "link": link}
    )
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send(
        fail_silently=False,
    )
    # return f"The task: send_email_to_delete to the user {email} was started"
    return link


def send_email_with_ebay_answer(uuid=None):
    alert = get_object_or_404(Alert, uuid=uuid)
    email = alert.owner.email
    results = get_filtered_data(alert.search_term, 5)
    if results:
        subject, from_email, to = (
            f"Results of your search:{alert.search_term}.",
            settings.EMAIL_HOST_USER,
            email,
        )
        context = {"alert": alert, "results": results}
        text_content = get_template("ebay_results_email.txt").render(context)
        html_content = get_template("ebay_results_email.html").render(context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send(
            fail_silently=False,
        )
    return f"The task to send the email to the user {email} was started"