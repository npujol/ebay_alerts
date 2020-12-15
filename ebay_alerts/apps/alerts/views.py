from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status

from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Alert, Account
from .serializers import AlertSerializer, AlertsListSerializer
from .emails import send_email_to_delete_a_alert


class AlertViewSet(viewsets.ModelViewSet):
    """
    General ViewSet description

    list: List the alerts

    retrieve: Retrieve an alert

    update: Update an alert

    create: Create an alert

    partial_update: Patch an alert

    destroy: Delete an alert

    """

    permission_classes = (AllowAny,)
    serializer_class = AlertSerializer
    queryset = Alert.objects.all()
    lookup_field = "uuid"

    def get_serializer_class(self):
        if self.action == "list":
            return AlertsListSerializer
        return AlertSerializer

    def list(self, request, *args, **kwargs):
        email = self.request.data["email"]
        self.queryset = self.queryset.filter(owner__email=email)
        return super().list(self, request, *args, **kwargs)
