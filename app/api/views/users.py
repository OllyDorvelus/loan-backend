from rest_framework import viewsets
from app.api.serializers.users import UserCreateSerializer, UserSerializer
from app.users.models import User
from app.api.permissions import AuthenticatedCantPost


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AuthenticatedCantPost]
    lookup_field = 'customer__pk'

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'create':
            serializer_class = UserCreateSerializer
        return serializer_class
