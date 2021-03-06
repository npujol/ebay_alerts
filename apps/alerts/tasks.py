from celery import shared_task
from celery.utils.log import get_task_logger

from .emails import (
    send_email_after_create,
    send_email_to_delete,
    send_email_with_ebay_answer,
)
from .models import Alert

logger = get_task_logger(__name__)


@shared_task(name="send_email_with_ebay_answer_task")
def send_email_with_ebay_answer_task(uuid):
    """send_email_with_ebay_answer_task"""
    logger.info(f"Task: send_email_with_ebay_answer_task, alert: {uuid}")
    return send_email_with_ebay_answer(uuid)


@shared_task(name="send_creation_email_task")
def send_creation_email_task(uuid):
    """send_creation_email_task"""
    logger.info(f"Task: send_creation_email_task, alert: {uuid}")
    return send_email_after_create(uuid)


@shared_task(name="send_email_to_delete_task")
def send_email_to_delete_task(uuid, site_base):
    """send_email_to_delete_task"""
    logger.info(f"Task: send_email_to_delete_task, alert: {uuid}")
    return send_email_to_delete(uuid, site_base)


@shared_task(name="send_alert_email_every_x_minutes_task", ignore_result=True)
def send_alert_email_every_x_minutes_task(interval_time):
    """send_alert_email_every_x_minutes_task"""
    logger.info(f"Task: send_alert_email_every_{interval_time}_minutes_task")
    alerts = Alert.objects.email_every_minutes(interval_time).values()
    for a in alerts:
        uuid = a["uuid"]
        send_email_with_ebay_answer_task.apply_async(args=[uuid])
        logger.info(f"Task: send_email_with_ebay_answer_task whit uuid:{uuid}")
    logger.info("The tasks were initialized")
    return "The tasks were initialized"
