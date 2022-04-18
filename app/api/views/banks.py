from rest_framework import viewsets
from app.accounts.models import Bank
from app.api.serializers.banks import BankSerializer, BankCreateSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from app.api.permissions import IsAdminOrObjectOwner
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAdminOrObjectOwner]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "create" or self.action == "update":
            serializer_class = BankCreateSerializer
        return serializer_class

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "list":
            self.permission_classes = [IsAdminUser]
        return super(BankViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bank = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            BankSerializer(bank).data, status=HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(BankSerializer(instance).data)

    def perform_create(self, serializer):
        return serializer.save()
