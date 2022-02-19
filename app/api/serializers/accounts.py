from rest_framework import serializers
from app.accounts.models import LoanAccount
from djmoney.contrib.django_rest_framework import MoneyField
from datetime import date
from moneyed import ZAR


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanAccount
        fields = [
            'balance',
            'due_date',
            'status'
        ]


class CreateLoanApplicationSerializer(serializers.ModelSerializer):
    balance = MoneyField(write_only=True, max_digits=9, decimal_places=2, default_currency=ZAR)
    balance_confirm = MoneyField(write_only=True, max_digits=9, decimal_places=2, default_currency=ZAR)
    due_date = serializers.DateField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = LoanAccount
        fields = ('balance', 'balance_confirm', 'due_date', 'status')

    def validate(self, attrs):
        balance = attrs.get('balance')
        balance_confirm = attrs.get('balance_confirm')

        if balance != balance_confirm:
            msg = {'balance confirm': ['Balance amount must match.']}
            raise serializers.ValidationError(msg)

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            del validated_data['balance_confirm']
            validated_data['due_date'] = date(2099, 1, 1)
            validated_data['user'] = request.user
            return LoanAccount.objects.create_loan_account(**validated_data)