import pytest
from django.test import Client
from mixer.backend.django import mixer
from app.accounts.models import Bank, BankName
import json


client = Client()
BASE_URL = "/api/banks"


@pytest.fixture()
def bank_payload(db):
    return {"bank_name": "1", "bank_type": "1", "account_number": "1111111"}


def test_anon_cant_create_bank(bank_payload):
    response = client.post(f"{BASE_URL}/", bank_payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_anon_cant_view_banks():
    response = client.get(f"{BASE_URL}/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_anon_cant_delete_bank(bank):
    response = client.delete(f"{BASE_URL}/{bank.pk}/")
    assert response.status_code == 401


def test_anon_user_cant_edit_bank_info(bank_payload, bank):
    response = client.put(f"{BASE_URL}/{bank.pk}/", bank_payload)
    assert response.status_code == 401


def test_auth_cant_view_bank_list(auth_user):
    client.force_login(auth_user)
    response = client.get(f"{BASE_URL}/")
    assert response.status_code == 403


def test_auth_user_cant_view_other_banks(other_user, bank):
    client.force_login(other_user)
    response = client.get(f"{BASE_URL}/{bank.pk}/")
    assert response.status_code == 403


def test_auth_user_can_delete_their_bank(auth_user):
    client.force_login(auth_user)
    new_bank = mixer.blend(Bank, user=auth_user)
    response = client.delete(f"{BASE_URL}/{new_bank.pk}/")
    assert response.status_code == 204


def test_auth_user_can_view_their_bank(auth_user, bank):
    client.force_login(auth_user)
    response = client.get(f"{BASE_URL}/{bank.pk}/")
    assert response.status_code == 200


def test_auth_user_cant_delete_other_banks(other_user, bank):
    client.force_login(other_user)
    response = client.delete(f"{BASE_URL}/{bank.pk}/")
    assert response.status_code == 403


def test_auth_user_can_create_bank(auth_user, bank_type, bank_name, bank_payload):
    client.force_login(auth_user)
    bank_payload["bank_name"] = bank_name.pk
    bank_payload["bank_type"] = bank_type.pk
    response = client.post(f"{BASE_URL}/", bank_payload)
    assert response.status_code == 201


@pytest.mark.skip
def test_auth_user_can_edit_bank_info(auth_user, bank, bank_type, bank_payload):
    client.force_login(auth_user)
    new_bank_name = mixer.blend(BankName, name="Absa")
    bank_payload["bank_name"] = new_bank_name.pk
    bank_payload["bank_type"] = bank_type.pk
    bank_payload["id"] = bank.pk
    print("PAYLOAD", bank_payload)
    response = client.put(f"{BASE_URL}/{bank.pk}/", bank_payload)
    assert response.status_code == 200
    body = json.loads(response.content)
    assert body["bank_name"]["name"] == "Absa"


def test_user_cant_edit_other_user_bank_info(other_user, bank_payload, bank):
    client.force_login(other_user)
    response = client.put(f"{BASE_URL}/{bank.pk}/", bank_payload)
    assert response.status_code == 403
