from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView, mixins

from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Alert, Account
from .serializers import AlertSerializer, AlertsListSerializer, AccountSerializer
from .permissions import IsOwner
from .tasks import send_email_to_delete_task


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

    def list(self, request, *args, **kwargs):
        email = self.request.query_params.get("email", None)
        if email:
            self.queryset = self.queryset.filter(owner__email=email)
        return super().list(self, request, *args, **kwargs)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsOwner],
    )
    def email_to_delete(self, request, uuid=None):
        instance = get_object_or_404(Alert, uuid=uuid)
        send_email_to_delete_task.apply_async(
            args=[uuid, f"http://{request.get_host()}:{request.get_port()}"]
        )

        return Response(
            {"detail": "We are sending the email! You will receive the email soon."},
            status=status.HTTP_202_ACCEPTED,
        )


class AccountAlertsViewSet(viewsets.ModelViewSet):
    """
    General ViewSet description

    list: List the alerts for a user
    retrive:

    """

    permission_classes = (AllowAny,)
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    lookup_field = "uuid"
