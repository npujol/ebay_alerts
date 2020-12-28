from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "alerts"

router = DefaultRouter(trailing_slash=False)
router.register("alerts", views.AlertViewSet, basename="alert")
router.register("account", views.AccountAlertsViewSet, basename="account")


urlpatterns = [
    path("", include(router.urls)),
]
