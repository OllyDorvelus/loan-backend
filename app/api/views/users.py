from rest_framework import viewsets
from app.api.serializers.users import UserCreateSerializer, UserSerializer
from app.users.models import User
from app.api.permissions import AuthenticatedCantPost
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            UserSerializer(user).data, status=HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save()
