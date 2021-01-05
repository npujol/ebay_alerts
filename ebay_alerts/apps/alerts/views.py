from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Account, Alert
from .serializers import AccountSerializer, AlertSerializer
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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "uuid",
                openapi.IN_QUERY,
                description="uuid from the account",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={200: AlertSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """
        uuid -- The uuid for an account
        """
        account = self.request.query_params.get("uuid", None)
        if account:
            self.queryset = self.queryset.filter(owner__uuid=account)
        return super().list(self, request._request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            202: {
                "detail": "We are sending the email! You will receive the email soon."
            }
        },
    )
    @action(methods=["post"], detail=True)
    def email_to_delete(self, request, uuid=None):
        """
        Send an email to delete an alert
        """
        instance = self.get_object()
        send_email_to_delete_task.apply_async(
            args=[uuid, str(request.build_absolute_uri("/"))]
        )

        return Response(
            {"detail": "We are sending the email! You will receive the email soon."},
            status=status.HTTP_202_ACCEPTED,
        )


class AccountRetriveAPIView(RetrieveAPIView):
    """
    General ViewSet description
    retrieve: Get an account
    """

    permission_classes = (AllowAny,)
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    lookup_field = "uuid"
