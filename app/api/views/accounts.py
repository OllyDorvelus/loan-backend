from rest_framework import viewsets
from app.api.serializers.accounts import CreateLoanApplicationSerializer, AccountSerializer
from app.accounts.models import LoanAccount
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

APPLY_NAME = 'Apply Loan'


class AccountViewSet(viewsets.ModelViewSet):
    queryset = LoanAccount.objects.all()
    serializer_class = AccountSerializer

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.get_view_name() == APPLY_NAME:
            return CreateLoanApplicationSerializer
        return serializer

    @action(detail=False, methods=['post'], name=APPLY_NAME, permission_classes=[IsAuthenticated])
    def apply(self, request, pk=None, *args, **kwargs):
        """User can apply for a loan"""
        return super().create(request, *args, *kwargs)
