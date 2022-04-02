from django.test import TestCase
from mixer.backend.django import mixer
from app.users.models import User, Customer
from unittest.mock import patch


class UserModelsTestCase(TestCase):
    def setUp(self):
        self.user_one = mixer.blend(
            User, first_name="First", last_name="Last", phone_number="+11234567896"
        )
        self.customer_one = mixer.blend(Customer, user=self.user_one)

    def test_full_name_property(self):
        """Animals that can speak are correctly identified"""
        self.assertEqual(self.user_one.full_name, "First Last")

    def test_whatsapp_property(self):
        self.assertEqual(self.user_one.whatsapp_number, "whatsapp:+11234567896")

    def test_user_to_str(self):
        self.assertEqual(str(self.user_one), "First Last - +11234567896")

    def test_customer_to_str(self):
        self.assertEqual(str(self.customer_one), "First Last - +11234567896")

    @patch("app.api.whats_app_client.WhatsAppClient.send_account_created_message")
    def test_signal_is_not_ran_when_user_is_updated(self, mock):
        self.user_one.save()
        self.assertFalse(mock.called)
        self.assertEqual(mock.call_count, 0)

    @patch("app.api.whats_app_client.WhatsAppClient.send_account_created_message")
    def test_signal_is_called_when_user_is_created(self, mock):
        mixer.blend(User)
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)
