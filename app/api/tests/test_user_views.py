from django.test import TestCase
from mixer.backend.django import mixer
from app.api.serializers.users import UserCreateSerializer
from copy import deepcopy


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.serializer_data = {
            "email": "email@email.com",
            "email_confirm": "email@email.com",
            "first_name": "First",
            "last_name": "Last",
            "password": "password",
            "password_confirm": "password",
            "phone_number": "+12345678901",
            "phone_number_confirm": "+12345678901",
        }

    def test_successful_serializer_data(self):
        no_email_serializer_data = deepcopy(self.serializer_data)
        no_email_serializer_data.pop("email")
        no_email_serializer_data.pop("email_confirm")
        user_create_serializer = UserCreateSerializer(data=self.serializer_data)
        no_email_create_user_serializer = UserCreateSerializer(
            data=no_email_serializer_data
        )
        self.assertTrue(user_create_serializer.is_valid())
        user = user_create_serializer.create(self.serializer_data)
        self.assertTrue(user.customer)
        self.assertTrue(no_email_create_user_serializer.is_valid())

    def test_emails_dont_match_invalid_serializer_data(self):
        mismatch_emails_serializer_data = deepcopy(self.serializer_data)
        mismatch_emails_serializer_data["email_confirm"] = "email@emai.com"
        user_create_serializer = UserCreateSerializer(
            data=mismatch_emails_serializer_data
        )
        self.assertFalse(user_create_serializer.is_valid())

    def test_passwords_dont_match_invalid_serializer_data(self):
        mismatch_passwords_serializer_data = deepcopy(self.serializer_data)
        mismatch_passwords_serializer_data["password_confirm"] = "passwor"
        user_create_serializer = UserCreateSerializer(
            data=mismatch_passwords_serializer_data
        )
        self.assertFalse(user_create_serializer.is_valid())

    def test_phone_numbers_dont_match_phone_number_serializer(self):
        mismatch_emails_serializer_data = deepcopy(self.serializer_data)
        mismatch_emails_serializer_data["phone_number_confirm"] = "+12345678900"
        user_create_serializer = UserCreateSerializer(
            data=mismatch_emails_serializer_data
        )
        self.assertFalse(user_create_serializer.is_valid())
