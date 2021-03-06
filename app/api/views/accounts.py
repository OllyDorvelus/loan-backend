from rest_framework import viewsets
from app.api.serializers.accounts import (
    CreateLoanApplicationSerializer,
    AccountSerializer,
)
from app.accounts.models import LoanAccount
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from app.api.permissions import IsAdminOrUserOwnerReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAdminUser

APPLY_NAME = "Apply Loan"


class AccountViewSet(viewsets.ModelViewSet):
    queryset = LoanAccount.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action == "retrieve":
            self.permission_classes = [IsAdminOrUserOwnerReadOnly]
        return super(AccountViewSet, self).get_permissions()

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.get_view_name() == APPLY_NAME:
            return CreateLoanApplicationSerializer
        return serializer

    @action(
        detail=False,
        methods=["post"],
        name=APPLY_NAME,
        permission_classes=[IsAuthenticated],
    )
    def apply(self, request, *args, **kwargs):
        """User can apply for a loan"""
        user = request.user
        if user.accounts.count() > 0:
            return Response(
                {
                    "message": "You already applied for a loan and have an account with us."
                },
                status=HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, *kwargs)
