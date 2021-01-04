from unittest import skip

from hypothesis import HealthCheck, Verbosity, assume, given, settings
from hypothesis.extra.django import TestCase, from_model

from ..emails import send_email_to_delete
from ..models import Account, Alert


class TestEmails(TestCase):
    @settings(max_examples=1)
    @given(from_model(Alert, owner=from_model(Account)))
    def test_send_email_to_delete(self, alert):
        msg = send_email_to_delete(alert.uuid)
        assert True
