from django.db import transaction
from rest_framework import serializers

from .models import Account, Alert
from .tasks import send_creation_email_task


class AccountSerializer(serializers.ModelSerializer):
    alerts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ("uuid", "email", "alerts")
        read_only_fields = fields


class AlertSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    owner = AccountSerializer(read_only=True)

    class Meta:
        model = Alert
        fields = ("uuid", "owner", "search_term", "interval_time", "email")

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data["email"]
        if email:
            account, _ = Account.objects.get_or_create(email=email)
            del validated_data["email"]
            validated_data["owner"] = account
        print(self.context["request"])
        instance, _ = Alert.objects.get_or_create(**validated_data)
        transaction.on_commit(
            lambda: send_creation_email_task.apply_async(args=[instance.uuid])
        )
        return instance
