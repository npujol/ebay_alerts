from django.urls import reverse
from django.test import TestCase
from rest_framework import status


class URLsTestCase(TestCase):
    def test_create_alert_with_an_account(self):
        url = reverse("index")
        response = self.client.get(
            url,
        )
        self.assertRedirects(response, "/api/swagger/", status.HTTP_302_FOUND)
