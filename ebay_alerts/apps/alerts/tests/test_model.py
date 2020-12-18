from hypothesis import assume, given, HealthCheck, Verbosity, settings
from hypothesis.extra.django import (
    TestCase,
    from_model,
)
from hypothesis.strategies import lists
from ..models import Alert, Account


class TestAlertModel(TestCase):
    @given(from_model(Alert, owner=from_model(Account)))
    def test_is_alert(self, alert):
        self.assertIsInstance(alert, Alert)
        self.assertIsNotNone(alert.uuid)
        self.assertIsNotNone(alert.search_term)
        self.assertIsNotNone(alert.owner)
        self.assertIsNotNone(alert.interval_time)

    @given(from_model(Alert, owner=from_model(Account)))
    def test_can_get_a_alert(self, alert):
        assert alert.uuid

    @given(from_model(Account))
    def test_create_a_alert_with_an_account(self, account):
        alert = Alert.objects.create(
            owner=account, search_term="test term", interval_time="30"
        )
        assert alert.owner, email

    @given(from_model(Alert, owner=from_model(Account)))
    def test_no_null_in_charfield(self, alert):
        assert "\x00" not in alert.search_term


class TestAccountModel(TestCase):
    @given(from_model(Account))
    def test_is_account(self, account):
        self.assertIsInstance(account, Account)
        self.assertIsNotNone(account.uuid)
        self.assertIsNotNone(account.email)
        self.assertIsNotNone(account.alerts)

    @given(from_model(Account))
    def test_can_get_a_account(self, account):
        assert account.uuid

    @settings(suppress_health_check=HealthCheck.all(), verbosity=Verbosity.quiet)
    @given(lists(from_model(Account)))
    def test_can_get_multiple_models_with_unique_field(self, accounts):
        assume(len(accounts) > 1)
        for a in accounts:
            self.assertIsNotNone(a.uuid)
        assert len({a.uuid for a in accounts}), len({a.email for a in accounts})


class TestAlertModel2(TestCase):
    @given(from_model(Alert, owner=from_model(Account)))
    def test_need_to_send_email(self, alert):

        response = Alert.objects.email_every_thirty_minutes().values()
        assert isinstance(response, list)