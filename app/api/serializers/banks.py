from rest_framework import serializers
from app.accounts.models import Bank, BankName, BankType


class BankNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankName
        fields = (
            "id",
            "name",
        )


class BankTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankType
        fields = (
            "id",
            "type",
        )


class BankSerializer(serializers.ModelSerializer):
    bank_name = BankNameSerializer(read_only=True)
    bank_type = BankTypeSerializer(read_only=True)

    class Meta:
        model = Bank
        fields = ("id", "bank_name", "bank_type", "account_number")


class BankCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a bank"""

    class Meta:
        model = Bank
        fields = "__all__"
