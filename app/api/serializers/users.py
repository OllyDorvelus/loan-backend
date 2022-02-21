from rest_framework import serializers
from app.users.models import User, Customer
from phonenumber_field.serializerfields import PhoneNumberField
from django.db import transaction


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            'id',
            'active',
            'phone_number',
        ]

        read_only_fields = [
            'active',
        ]


class UserSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'customer',
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    password_confirm = serializers.CharField(min_length=8, trim_whitespace=False, style={'input_type': 'password'},
                                      write_only=True)
    email_confirm = serializers.EmailField(trim_whitespace=True, style={'input_type': 'email'}, write_only=True)
    phone_number = PhoneNumberField(write_only=True)
    phone_number_confirm = PhoneNumberField(write_only=True)

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8, 'style': {'input_type': 'password'}}}
        fields = ('email', 'email_confirm', 'first_name', 'last_name', 'password', 'password_confirm', 'phone_number', 'phone_number_confirm')

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        email = attrs.get('email')
        email_confirm = attrs.get('email_confirm')
        phone_number = attrs.get('phone_number')
        phone_number_confirm = attrs.get('phone_number_confirm')

        if password != password_confirm:
            msg = {'password_confirm': ['Passwords must match.']}
            raise serializers.ValidationError(msg)

        if email != email_confirm:
            msg = {'email_confirm': ['Emails must match.']}
            raise serializers.ValidationError(msg)

        if phone_number != phone_number_confirm:
            msg = {'phone_number': ['Phone numbers must match.']}
            raise serializers.ValidationError(msg)

        return attrs

    def create(self, validated_data):
        """"Create a new user with encrypted password and return it"""
        del validated_data['password_confirm']
        del validated_data['email_confirm']
        del validated_data['phone_number_confirm']
        phone_number = validated_data.pop('phone_number')

        # ensure nothing gets created in case of failure.
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            Customer.objects.create_customer(user=user, phone_number=phone_number)
            return user

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
