from hypothesis import assume, given, HealthCheck, Verbosity, settings
from hypothesis.extra.django import (
    TestCase,
    from_model,
)
from hypothesis.strategies import lists
from ..models import Alert, Account
from ..serializers import AlertSerializer, AccountSerializer


class TestAlertSerializer(TestCase):
    def setUp(self):
        account = Account.objects.create(email="test@email.email")
        self.alert_attributes = {
            "owner": account,
            "search_term": "test term",
            "interval_time": "30",
        }
        self.alert = Alert.objects.create(**self.alert_attributes)
        self.serializer = AlertSerializer(instance=self.alert)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(["uuid", "owner", "search_term", "interval_time"]),
        )

    def test_contains_expected_write_only_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(["uuid", "owner", "search_term", "interval_time"]),
        )

    def test_interval_time_must_be_in_choices(self):
        self.alert_attributes["interval_time"] = "54"

        serializer = AlertSerializer(instance=self.alert, data=self.alert_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertTrue("interval_time" in serializer.errors.keys())
