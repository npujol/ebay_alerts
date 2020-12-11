from rest_framework import viewsets

from rest_framework.permissions import AllowAny
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

    queryset = Alert.objects.select_related("owner", "owner__email")

    def list(self, request, *args, **kwargs):
        owner = self.request.query_params.get("owner", None)

        if owner is not None:
            self.queryset = self.queryset.filter(owner__email=owner)
        return super().list(self, request, *args, **kwargs)


    