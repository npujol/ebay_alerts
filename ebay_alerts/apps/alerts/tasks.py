from celery.utils.log import get_task_logger

from celery import shared_task
from .emails import (
    send_email_after_create,
    send_email_with_ebay_answer,
    send_email_to_delete,
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
def send_email_to_delete_task(uuid):
    """send_email_to_delete_task"""
    logger.info(f"Task: send_email_to_delete_task, alert: {uuid}")
    return send_email_to_delete(uuid)


@shared_task(
    name="send_alert_email_every_two_minutes_task",
    ignore_result=True,
)
def send_alert_email_every_two_minutes_task():
    """send_alert_email_every_two_minutes_task"""
    logger.info(f"Task: send_alert_email_every_two_minutes_task")
    alerts = Alert.objects.email_every_two_minutes().values()
    for a in alerts:
        uuid = a["uuid"]
        print(uuid)
        send_email_with_ebay_answer_task.apply_async(args=[uuid])
        logger.info(f"Task: send_email_with_ebay_answer_task whit uuid:{uuid}")
    logger.info("The tasks were initialized")
    return "The tasks were initialized"


@shared_task(
    name="send_alert_email_every_ten_minutes_task",
)
def send_alert_email_every_ten_minutes_task():
    """send_alert_email_every_ten_minutes_task"""
    logger.info("Task:send_alert_email_every_ten_minutes_task")
    alerts = Alert.objects.email_every_ten_minutes().values()
    for a in alerts:
        uuid = a["uuid"]
        send_email_with_ebay_answer_task.apply_async(args=[uuid])
        logger.info(f"Task: send_email_with_ebay_answer_task whit uuid:{uuid}")
    logger.info("The tasks were initialized")
    return "The tasks were initialized"


@shared_task(
    name="send_alert_email_every_thirty_minutes_task",
)
def send_alert_email_every_thirty_minutes_task():
    """send_alert_email_every_thirty_minutes_task"""
    logger.info("send_alert_email_every_thirty_minutes_task")
    alerts = Alert.objects.email_every_thirty_minutes().values()
    for a in alerts:
        uuid = a["uuid"]
        send_email_with_ebay_answer_task.apply_async(args=[uuid])
        logger.info(f"Task: send_email_with_ebay_answer_task whit uuid:{uuid}")
    logger.info("The tasks were initialized")
    return "The tasks were initialized"