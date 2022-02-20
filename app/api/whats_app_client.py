import os
from twilio.rest import Client

account_sid = os.getenv('WA_ACCOUNT_SID')
auth_token = os.getenv('WA_AUTH_TOKEN')
FROM_NUMBER = os.getenv('WA_FROM_NUMBER')
client = Client(account_sid, auth_token)


class WhatsAppClient:

    @staticmethod
    def send_message(msg, to_number):
        client.messages.create(
            body=msg,
            from_=FROM_NUMBER,
            to=to_number
        )

    @staticmethod
    def send_welcome_message(to_number):
        msg = f'Your account was created for Demifusion, thank you for banking with us.'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_accept_notice(to_number, first_name, last_name, balance, due_date, accepted_date):
        msg = f'Hi {first_name} {last_name}, Your balance of {balance} was accepted on {accepted_date} and is due on {due_date}'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_payment_reminder(to_number, first_name, last_name, balance, due_date):
        msg = f'Hi {first_name} {last_name}, This is a reminder your payment of {balance} is due on the {due_date}'
        WhatsAppClient.send_message(msg, to_number)
