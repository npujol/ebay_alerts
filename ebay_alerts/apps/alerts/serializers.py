from rest_framework import serializers
from .models import Alert, Account


class AccountSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Alert
        fields = ("id", "email")
        lookup_field = "id"


class AlertSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    owner = AccountSerializer(read_only=True)

    class Meta:
        model = Alert
        fields = ("id", "owner", "search_term", "interval_time")
        lookup_field = "id"


class AlertHyperlink(serializers.HyperlinkedRelatedField):
    # We define these as class attributes, so we don't need to pass them as arguments.
    view_name = "alert-detail"
    queryset = Alert.objects.all()

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {"owner__email": obj.owner.email, "id": obj.id}
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            "owner__email": view_kwargs["owner__email"],
            "id": view_kwargs["id"],
        }
        return self.get_queryset().get(**lookup_kwargs)
