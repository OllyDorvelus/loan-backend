from rest_framework import viewsets
from app.accounts.models import Bank
from app.api.serializers.banks import BankSerializer, BankCreateSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from app.api.permissions import IsAdminOrObjectOwner


class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAdminOrObjectOwner]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "create":
            serializer_class = BankCreateSerializer
        return serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bank = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            BankSerializer(bank).data, status=HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save()
