import pytest
from unittest.mock import patch
from mixer.backend.django import mixer
from app.users.models import User, Customer


@pytest.fixture()
def user(db):
    return mixer.blend(
        User, first_name="First", last_name="Last", phone_number="+11234567896"
    )


@pytest.fixture()
def customer(db, user):
    return mixer.blend(Customer, user=user)


def test_full_name_property(user):
    assert user.full_name == "First Last"


def test_whatsapp_property(user):
    assert user.whatsapp_number == "whatsapp:+11234567896"


def test_user_to_str(user):
    assert str(user) == "First Last - +11234567896"


def test_customer_to_str(customer):
    assert str(customer) == "First Last - +11234567896"


@patch("app.api.whats_app_client.WhatsAppClient.send_account_created_message")
def test_signal_is_not_ran_when_user_is_updated(mock, user):
    user.save()
    assert mock.called is False
    assert mock.call_count == 0


@patch("app.api.whats_app_client.WhatsAppClient.send_account_created_message")
@pytest.mark.django_db
def test_signal_is_called_when_user_is_created(mock):
    mixer.blend(User)
    assert mock.called is True
    assert mock.call_count == 1
