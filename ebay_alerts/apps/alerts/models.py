import uuid

from django.db import models


class BaseModel(models.Model):
    uuid = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Account(BaseModel):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class AlertQuerySet(models.QuerySet):
    def email_every_minutes(self, interval_time):
        return self.filter(interval_time=interval_time)


class Alert(BaseModel):
    class IntervalOfTime(models.TextChoices):
        TWO = 2, "2 minutes"
        TEN = 10, "10 minutes"
        THIRTY = 30, "30 minutes"

    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="alerts")
    search_term = models.CharField(max_length=250)
    interval_time = models.CharField(
        max_length=2, choices=IntervalOfTime.choices, default=IntervalOfTime.THIRTY
    )

    objects = AlertQuerySet.as_manager()

    class Meta:
        unique_together = [["search_term", "interval_time", "owner"]]
        ordering = ["updated_at"]

    def __str__(self):
        return f"Alert number: {self.uuid}"
