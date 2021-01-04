from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "alerts"

router = DefaultRouter(trailing_slash=False)
router.register("alerts", views.AlertViewSet, basename="alert")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "accounts/<uuid:uuid>",
        views.AccountRetriveAPIView.as_view(),
        name="account-retrive",
    ),
]
