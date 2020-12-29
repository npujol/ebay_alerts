from hypothesis import assume, given, HealthCheck, Verbosity, settings
from hypothesis.extra.django import (
    TestCase,
    from_model,
)
from unittest import skip
from ..models import Alert, Account
from ..emails import send_email_to_delete


class TestEmails(TestCase):
    @settings(max_examples=1)
    @given(from_model(Alert, owner=from_model(Account)))
    def test_send_email_to_delete(self, alert):
        msg = send_email_to_delete(alert.uuid)
        print(msg)
        assert True