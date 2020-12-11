from .test_base import BaseRestTestCase

from django.urls import reverse
from rest_framework import status

from ..models import Alert, Account
from ..serializers import Alert


class AlertListCreateAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("alerts:alert-list")

    def test_create_alert(self):
        alerts_count = Alert.objects.all().count()

        response = self.client.post(
            self.url,
            {
                "owner": "test2@email.com",
                "search_term": "string",
                "interval_time": "30",
            },
        )
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Alert.objects.all().count(), (alerts_count + 1))
        self.assertEqual(Alert.objects.last().owner.email, "test2@email.com")

    def test_empty_list_alerts(self):
        """
        Test to verify alerts list
        """
        response = self.client.get(
            self.url, **{"QUERY_STRING": "owner=test2@email.com"}
        )
        self.assertEqual(response.json().get("count"), Alert.objects.all().count())


class AlertDetailAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.alert = Alert.objects.create(
            owner="test2@email.com",
            search_term="string",
            interval_time="2",
        )
        self.url = reverse(
            "alerts:alert-detail",
            kwargs={"id": self.alert.id},
        )

    def test_alert_object_detail(self):
        """
        Test to verify a alert object detail
        """
        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)

    def test_alert_object_update(self):
        response = self.client.put(
            self.url,
            {
                "owner": "test2@email.com",
                "search_term": "string",
                "interval_time": "10",
            },
            **{
                "QUERY_STRING": "owner=test2@email.com",
            }
        )

        alert = Alert.objects.get(id=self.alert.id)
        self.assertEqual(response.json().get("owner"), alert.owner)

    def test_alert_object_partial_update(self):
        response = self.client.patch(
            self.url,
            {"search_term": "string2"},
        )

        alert = Alert.objects.get(id=self.alert.id)
        self.assertEqual(response.json().get("search_term"), alert.search_term)

    def test_alert_object_delete(self):
        response = self.client.delete(self.url)

        self.assertEqual(204, response.status_code)
