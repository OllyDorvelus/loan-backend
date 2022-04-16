from django.urls import path
from django.urls import include
from app.api.views.users import UserViewSet
from app.api.views.accounts import AccountViewSet
from app.api.views.banks import BankViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", UserViewSet, basename="api-users")
router.register("accounts", AccountViewSet, basename="api-accounts")
router.register("banks", BankViewSet, basename="api-banks")

urlpatterns = [
    path("", include(router.urls)),
]
