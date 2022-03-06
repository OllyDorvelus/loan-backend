from rest_framework import viewsets
from app.api.serializers.users import UserCreateSerializer, UserSerializer
from app.users.models import User
from app.api.permissions import AuthenticatedCantPost
from rest_framework.permissions import IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "customer__pk"

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "create":
            serializer_class = UserCreateSerializer
        return serializer_class

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AuthenticatedCantPost]
        return super(UserViewSet, self).get_permissions()
