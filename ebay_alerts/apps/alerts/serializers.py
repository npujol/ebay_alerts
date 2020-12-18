from django.db import IntegrityError, transaction
from rest_framework import serializers
from .models import Alert, Account
from .tasks import send_creation_email_task


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("email",)


class AlertSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    owner = AccountSerializer(read_only=True)

    class Meta:
        model = Alert
        fields = (
            "uuid",
            "owner",
            "search_term",
            "interval_time",
            "email",
        )

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data["email"]
        if email:
            account, _ = Account.objects.get_or_create(email=email)
            del validated_data["email"]
            validated_data["owner"] = account

        instance = Alert.objects.create(**validated_data)
        transaction.on_commit(
            lambda: send_creation_email_task.apply_async(args=[instance.uuid])
        )
        return instance


class AlertsListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Alert
        fields = (
            "uuid",
            "search_term",
            "interval_time",
            "email",
        )