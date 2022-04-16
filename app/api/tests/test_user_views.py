import pytest
from django.test import Client
import json
from app.api.serializers.users import UserCreateSerializer
from copy import deepcopy


BASE_URL = "/api/users"
client = Client()


@pytest.fixture()
def serializer_data():
    return {
        "email": "email@email.com",
        "email_confirm": "email@email.com",
        "first_name": "First",
        "last_name": "Last",
        "password": "password",
        "password_confirm": "password",
        "phone_number": "+12345678901",
        "phone_number_confirm": "+12345678901",
    }


@pytest.mark.django_db
def test_successful_serializer_data(serializer_data):
    no_email_serializer_data = deepcopy(serializer_data)
    no_email_serializer_data.pop("email")
    no_email_serializer_data.pop("email_confirm")
    user_create_serializer = UserCreateSerializer(data=serializer_data)
    no_email_create_user_serializer = UserCreateSerializer(
        data=no_email_serializer_data
    )
    assert user_create_serializer.is_valid()
    user = user_create_serializer.create(serializer_data)
    assert user.customer
    assert no_email_create_user_serializer.is_valid()


@pytest.mark.django_db
def test_emails_dont_match_invalid_serializer_data(serializer_data):
    mismatch_emails_serializer_data = deepcopy(serializer_data)
    mismatch_emails_serializer_data["email_confirm"] = "email@emai.com"
    user_create_serializer = UserCreateSerializer(data=mismatch_emails_serializer_data)
    assert user_create_serializer.is_valid() is False


def test_passwords_dont_match_invalid_serializer_data(serializer_data):
    mismatch_passwords_serializer_data = deepcopy(serializer_data)
    mismatch_passwords_serializer_data["password_confirm"] = "passwor"
    user_create_serializer = UserCreateSerializer(
        data=mismatch_passwords_serializer_data
    )
    assert user_create_serializer.is_valid() is False


def test_phone_numbers_dont_match_phone_number_serializer(serializer_data):
    mismatch_emails_serializer_data = deepcopy(serializer_data)
    mismatch_emails_serializer_data["phone_number_confirm"] = "+12345678900"
    user_create_serializer = UserCreateSerializer(data=mismatch_emails_serializer_data)
    assert user_create_serializer.is_valid() is False


def test_anon_user_cant_view_users_list_and_detail(auth_user):
    response = client.get(f"{BASE_URL}/")
    assert response.status_code == 401
    response = client.get(f"{BASE_URL}/{auth_user.customer.pk}/")
    assert response.status_code == 401


def test_auth_user_cant_view_users_list(auth_user):
    client.force_login(auth_user)
    response = client.get(f"{BASE_URL}/")
    assert response.status_code == 403


def test_admin_can_view_users_list(admin_user):
    client.force_login(admin_user)
    response = client.get(f"{BASE_URL}/")
    assert response.status_code == 200


def test_user_can_view_own_info_but_cant_view_others(auth_user, other_user):
    client.force_login(auth_user)
    response = client.get(f"{BASE_URL}/{auth_user.customer.pk}/")
    assert response.status_code == 200
    body = json.loads(response.content)
    assert body["first_name"] == "First"
    response = client.get(f"{BASE_URL}/{other_user.customer.pk}/")
    assert response.status_code == 403


def test_admin_can_view_any_user(admin_user, auth_user):
    client.force_login(admin_user)
    response = client.get(f"{BASE_URL}/{auth_user.customer.pk}/")
    body = json.loads(response.content)
    assert response.status_code == 200
    assert body["first_name"] == "First"


def test_auth_user_cant_create_user(auth_user, serializer_data):
    client.force_login(auth_user)
    data = deepcopy(serializer_data)
    data["phone_number"] = "+12345678900"
    data["phone_number_confirm"] = "+12345678900"
    data["email"] = "email2@email.com"
    data["email_confirm"] = "email2@email.com"
    response = client.post(f"{BASE_URL}/", data)
    assert response.status_code == 403
