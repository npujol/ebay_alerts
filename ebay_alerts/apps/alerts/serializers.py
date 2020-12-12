from rest_framework import serializers
from .models import Alert, Account


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

    def create(self, validated_data):
        email = validated_data["email"]
        if email:
            account, _ = Account.objects.get_or_create(email=email)
            del validated_data["email"]
            validated_data["owner"] = account
        return Alert.objects.create(**validated_data)
