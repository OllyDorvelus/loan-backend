from mixer.backend.django import mixer
from app.users.models import User
from app.accounts.models import LoanAccount, Bank, BankName, BankType, Transaction
from unittest.mock import patch
import pytest


default_amount = (10.00, "ZAR")


@pytest.fixture()
def data(db):
    user = mixer.blend(User, first_name="First", last_name="Last")
    bank_type = mixer.blend(BankType, type=BankType.SAVINGS)
    bank_name = mixer.blend(BankName, name="Chase")
    bank = mixer.blend(
        Bank,
        user=user,
        bank_name=bank_name,
        type=bank_type,
        account_number="11111111",
    )
    account = mixer.blend(LoanAccount, user=user, principal=default_amount)
    transaction = mixer.blend(Transaction, amount=(10.00, "ZAR"), account=account)
    return {
        "user": user,
        "bank_type": bank_type,
        "bank_name": bank_name,
        "bank": bank,
        "account": account,
        "transaction": transaction,
    }


def test_bank_to_str(data):
    assert str(data["bank"]) == "First Last - Chase - 11111111"
    assert str(data["bank"]) == "First Last - Chase - 11111111"


def test_bank_type_to_str(data):
    assert str(data["bank_type"]) == "SAVINGS"


def test_bank_name_to_str(data):
    assert str(data["bank_name"]) == "Chase"


def test_account_to_str(data):
    assert str(data["account"]) == "First Last - 10.00 - 12.50"


def test_transaction_to_str(data):
    assert str(data["transaction"]) == "First Last - R10,00"


@patch("app.api.whats_app_client.WhatsAppClient.send_submitted_application_message")
@pytest.mark.django_db
def test_send_submitted_application_message_send_when_account_created(mock):
    mixer.blend(LoanAccount, principal=default_amount)
    assert mock.called is True
    assert mock.called == 1


@patch("app.api.whats_app_client.WhatsAppClient.send_submitted_application_message")
def test_send_submitted_application_message_not_called_on_exisiting_account_update(
    mock, data
):
    account = data["account"]
    account.save()
    assert mock.called is False
    assert mock.call_count == 0


@patch("app.api.whats_app_client.WhatsAppClient.send_balance_change_message")
@pytest.mark.django_db
def test_send_balance_change_and_transaction_created(mock):
    account = mixer.blend(LoanAccount, principal=default_amount)
    account.add(5.00)
    account.subtract(2.00)
    assert mock.called is True
    assert mock.call_count == 3


@patch("app.api.whats_app_client.WhatsAppClient.send_balance_change_message")
@pytest.mark.django_db
def test_no_balance_change_and_no_transaction_when_balance_remains_the_same(mock):
    account = mixer.blend(LoanAccount, principal=default_amount)
    account.add(0.00)
    account.subtract(0.00)
    assert mock.call_count == 1


@patch("app.api.whats_app_client.WhatsAppClient.send_close_message")
@pytest.mark.django_db
def test_account_close_message(mock):
    account = mixer.blend(LoanAccount, principal=default_amount)
    account.status = LoanAccount.CLOSED
    account.save()
    assert mock.called is True
    assert mock.call_count == 1


@patch("app.api.whats_app_client.WhatsAppClient.send_close_message")
@pytest.mark.django_db
def test_account_close_message_not_called(mock):
    account = mixer.blend(LoanAccount, principal=default_amount)
    account.save()
    assert mock.called is False
    assert mock.call_count == 0


@pytest.mark.django_db
def test_add_account_method():
    account = mixer.blend(LoanAccount, principal=default_amount)
    account.add(5.50)
    assert account.balance.amount == 18.00
    assert account.principal.amount == 10.00
    transaction = account.transactions.latest("created")
    assert transaction.amount.amount == 5.50


@pytest.mark.django_db
def test_subtract_account_method():
    account = mixer.blend(LoanAccount, principal=default_amount)
    account.subtract(5.50)
    assert account.balance.amount == 7.00
    assert account.principal.amount == 10.00
    transaction = account.transactions.latest("created")
    assert transaction.amount.amount == -5.50
