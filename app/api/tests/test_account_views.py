import pytest
import json
from django.test import Client

BASE_URL = "/api/accounts"

client = Client()
default_amount = (10.00, "ZAR")


@pytest.fixture()
def apply_payload():
    return {
        "principal": 10.00,
        "principal_confirm": 10.00,
    }


def test_anon_cant_view_accounts(auth_account):
    response = client.get(f"{BASE_URL}/")
    assert response.status_code == 401
    response = client.get(f"{BASE_URL}/{auth_account.pk}/")
    assert response.status_code == 401


def test_auth_user_cant_view_accounts_list(auth_user):
    client.force_login(auth_user)
    response = client.get(f"{BASE_URL}/")
    assert response.status_code == 403


def test_auth_user_cant_view_other_accounts(auth_account, other_user):
    client.force_login(other_user)
    response = client.get(f"{BASE_URL}/{auth_account.pk}/")
    assert response.status_code == 403


def test_auth_user_can_view_their_accounts(auth_user, auth_account):
    client.force_login(auth_user)
    response = client.get(f"{BASE_URL}/{auth_account.pk}/")
    assert response.status_code == 200
    body = json.loads(response.content)
    assert body["user"]["first_name"] == "First"


def test_admin_user_can_view_all(admin_user, auth_account):
    client.force_login(admin_user)
    response = client.get(f"{BASE_URL}/{auth_account.pk}/")
    assert response.status_code == 200
    response = client.get(f"{BASE_URL}/")
    assert response.status_code == 200


def test_auth_user_can_apply_for_loan_once(other_user, apply_payload):
    client.force_login(other_user)
    response = client.post(f"{BASE_URL}/apply/", apply_payload)
    assert response.status_code == 201
    response = client.post(f"{BASE_URL}/apply/", apply_payload)
    assert response.status_code == 400


def test_auth_user_cant_delete_account(auth_user, auth_account):
    client.force_login(auth_user)
    response = client.delete(f"{BASE_URL}/{auth_account.pk}/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_anon_user_cant_apply_for_loan(apply_payload):
    response = client.post(f"{BASE_URL}/apply/", apply_payload)
    assert response.status_code == 401
