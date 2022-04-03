from django.test import TestCase
from mixer.backend.django import mixer
from app.users.models import User
from app.accounts.models import LoanAccount, Bank, BankName, BankType, Transaction
from unittest.mock import patch


class AccountModelsTestCase(TestCase):
    def setUp(self):
        self.default_amount = (10.00, "ZAR")
        self.user_one = mixer.blend(User, first_name="First", last_name="Last")
        self.bank_type = mixer.blend(BankType, type=BankType.SAVINGS)
        self.bank_name = mixer.blend(BankName, name="Chase")
        self.bank = mixer.blend(
            Bank,
            user=self.user_one,
            bank_name=self.bank_name,
            type=self.bank_type,
            account_number="11111111",
        )
        self.account_one = mixer.blend(
            LoanAccount, user=self.user_one, principal=self.default_amount
        )
        self.transaction_one = mixer.blend(
            Transaction, amount=(10.00, "ZAR"), account=self.account_one
        )

    def test_bank_to_str(self):
        self.assertEqual(str(self.bank), "First Last - Chase - 11111111")

    def test_bank_type_to_str(self):
        self.assertEqual(str(self.bank_type), "SAVINGS")

    def test_bank_name_to_str(self):
        self.assertEqual(str(self.bank_name), "Chase")

    def test_account_to_str(self):
        self.assertEqual(str(self.account_one), "First Last - 10.00 - 12.50")

    def test_transaction_to_str(self):
        self.assertEqual(str(self.transaction_one), "First Last - R10,00")

    @patch("app.api.whats_app_client.WhatsAppClient.send_submitted_application_message")
    def test_send_submitted_application_message_send_when_account_created(self, mock):
        mixer.blend(LoanAccount, principal=self.default_amount)
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)

    @patch("app.api.whats_app_client.WhatsAppClient.send_submitted_application_message")
    def test_send_submitted_application_message_not_called_on_exisiting_account_update(
        self, mock
    ):
        self.account_one.save()
        self.assertFalse(mock.called)
        self.assertEqual(mock.call_count, 0)

    @patch("app.api.whats_app_client.WhatsAppClient.send_balance_change_message")
    def test_send_balance_change_and_transaction_created(self, mock):
        account = mixer.blend(LoanAccount, principal=self.default_amount)
        account.add(5.00)
        account.subtract(2.00)
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 3)

    @patch("app.api.whats_app_client.WhatsAppClient.send_balance_change_message")
    def test_no_balance_change_and_no_transaction_when_balance_remains_the_same(
        self, mock
    ):
        account = mixer.blend(LoanAccount, principal=self.default_amount)
        account.add(0.00)
        account.subtract(0.00)
        self.assertEqual(mock.call_count, 1)

    @patch("app.api.whats_app_client.WhatsAppClient.send_close_message")
    def test_account_close_message(self, mock):
        account = mixer.blend(LoanAccount, principal=self.default_amount)
        account.status = LoanAccount.CLOSED
        account.save()
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)

    @patch("app.api.whats_app_client.WhatsAppClient.send_close_message")
    def test_account_close_message_not_called(self, mock):
        account = mixer.blend(LoanAccount, principal=self.default_amount)
        account.save()
        self.assertFalse(mock.called)
        self.assertEqual(mock.call_count, 0)

    def test_add_account_method(self):
        account = mixer.blend(LoanAccount, principal=self.default_amount)
        account.add(5.50)
        self.assertEqual(account.balance.amount, 18.00)
        self.assertEqual(account.principal.amount, 10.00)
        transaction = account.transactions.latest("created")
        self.assertEqual(transaction.amount.amount, 5.50)

    def test_subtract_account_method(self):
        account = mixer.blend(LoanAccount, principal=self.default_amount)
        account.subtract(5.50)
        self.assertEqual(account.balance.amount, 7.00)
        self.assertEqual(account.principal.amount, 10.00)
        transaction = account.transactions.latest("created")
        self.assertEqual(transaction.amount.amount, -5.50)
