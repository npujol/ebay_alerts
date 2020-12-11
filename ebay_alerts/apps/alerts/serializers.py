from rest_framework import serializers
from .models import Alert, Account


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ("id", "owner", "search_term", "interval_time")
