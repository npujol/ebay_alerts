from django.urls import reverse
from hypothesis import given, settings
from hypothesis.extra.django import TestCase, from_model
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Account, Alert


class AlertAPIViewTestCase(TestCase, APITestCase):
    def test_create_alert_with_an_account(self):
        url = reverse("alerts:alert-list")
        alerts_count = Alert.objects.all().count()
        account = Account.objects.create(email="test2@email.com")
        response = self.client.post(
            url,
            {
                "email": "test2@email.com",
                "search_term": "string",
                "interval_time": "30",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Alert.objects.all().count(), (alerts_count + 1))
        self.assertEqual(Alert.objects.last().owner.email, "test2@email.com")

    @settings(max_examples=1)
    def test_create_alert_without_an_account(self):
        url = reverse("alerts:alert-list")
        alerts_count = Alert.objects.all().count()
        response = self.client.post(
            url,
            {
                "email": "test3@email.com",
                "search_term": "string",
                "interval_time": "30",
            },
        )
        assert response.status_code, status.HTTP_201_CREATED
        assert Alert.objects.all().count(), alerts_count + 1
        assert Alert.objects.last().owner.email, "test3@email.com"

    @settings(max_examples=1)
    @given(from_model(Account))
    def test_empty_list_for_a_account(self, account):
        url = reverse("alerts:alert-list")
        response = self.client.get(
            url, data={"account": account.uuid}, HTTP_ACCEPT="application/json"
        )
        print(response)
        self.assertEquals(
            len(response.json()), Alert.objects.filter(owner=account).count()
        )

    @settings(max_examples=1)
    @given(from_model(Account))
    def test_list_for_a_account(self, account):
        Alert.objects.create(
            owner=account, search_term="test term2", interval_time="30"
        )
        url = reverse("alerts:alert-list")
        response = self.client.get(url, data={"account": account.uuid})
        self.assertEquals(
            len(response.json()), Alert.objects.filter(owner=account).count()
        )

    @settings(max_examples=1)
    @given(from_model(Alert, owner=from_model(Account)))
    def test_alert_get_object(self, alert):
        url = reverse("alerts:alert-detail", kwargs={"uuid": alert.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @settings(max_examples=1)
    @given(from_model(Alert, owner=from_model(Account)))
    def test_alert_object_partial_update_search_term(self, alert):
        url = reverse("alerts:alert-detail", kwargs={"uuid": alert.uuid})
        response = self.client.patch(url, {"search_term": "string2"})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(response.json()["search_term"], "string2")

    @settings(max_examples=1)
    @given(from_model(Alert, owner=from_model(Account)))
    def test_alert_object_partial_update_interval_time(self, alert):
        url = reverse("alerts:alert-detail", kwargs={"uuid": alert.uuid})
        response = self.client.patch(url, {"interval_time": "2"})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(response.json()["interval_time"], "2")

    @settings(max_examples=1)
    @given(from_model(Alert, owner=from_model(Account)))
    def test_alert_object_delete(self, alert):
        url = reverse("alerts:alert-detail", kwargs={"uuid": alert.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
