from datetime import date
from moneyed import ZAR
from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers
from app.accounts.models import LoanAccount, Bank
from app.api.serializers.users import UserSerializer


class BankSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Bank


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = LoanAccount
        fields = [
            "id",
            "balance",
            "due_date",
            "status",
            "user",
        ]


class CreateLoanApplicationSerializer(serializers.ModelSerializer):
    principal = MoneyField(
        write_only=True, max_digits=9, decimal_places=2, default_currency=ZAR
    )
    principal_confirm = MoneyField(
        write_only=True, max_digits=9, decimal_places=2, default_currency=ZAR
    )
    due_date = serializers.DateField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = LoanAccount
        fields = ("principal", "principal_confirm", "due_date", "status")

    def validate(self, attrs):
        principal = attrs.get("principal")
        principal_confirm = attrs.get("principal_confirm")

        if principal != principal_confirm:
            msg = {"principal confirm": ["Principal amount must match."]}
            raise serializers.ValidationError(msg)

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            del validated_data["principal_confirm"]
            validated_data["due_date"] = date(2099, 1, 1)
            validated_data["user"] = request.user
            return LoanAccount.objects.create_loan_account(
                **validated_data, status=LoanAccount.PENDING
            )
