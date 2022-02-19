from django.urls import path
from django.urls import include
from app.api.views.users import UserViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet, basename='api-users')

urlpatterns = [
    path('', include(router.urls)),
]
