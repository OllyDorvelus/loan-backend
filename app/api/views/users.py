from rest_framework import viewsets
from app.api.serializers.users import UserCreateSerializer, UserSerializer
from app.users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'create':
            serializer_class = UserCreateSerializer
        return serializer_class
