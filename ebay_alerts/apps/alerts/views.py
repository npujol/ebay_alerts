from rest_framework import viewsets, status

from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Alert, Account
from .serializers import AlertSerializer


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
        self.queryset = self.queryset.filter(owner__email=email)

        return super().list(self, request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_name="delete")
    def delete(self, request, uuid=None):
        return Response(
            {"message": "we will send you an email."},
            status=status.HTTP_202_ACCEPTED,
        )
