import os
from datetime import date
from twilio.rest import Client
from app.utils import format_date, apply_interest

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
    def send_welcome_message(to_number, first_name, last_name, amount):
        msg = f'Hi {first_name} {last_name} on {format_date(date.today())} for R{amount}, your loan application has been submitted to ' \
              f'Dimofusion and we will notify you on the status of your applicaiton.'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_accept_loan_message(to_number, first_name, last_name, balance, due_date, total):
        msg = f'Hi {first_name} {last_name} you have taken out a loan of R{balance}' \
              f'with Dimofusion at a 25% interest rate. The total debt payable on  {format_date(due_date)} is R{total}'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_payment_reminder(to_number, first_name, last_name, amount, due_date):
        msg = f'Hi {first_name} {last_name}, This is a reminder your payment of R{amount} is due on the {format_date(due_date)}'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_accept_notice(to_number, first_name, last_name, balance, due_date, accepted_date):
        msg = f'Hi {first_name} {last_name}, Your loan of R{balance} was accepted on {format_date(accepted_date)}' \
              f' by Dimofusion and is due on {format_date(due_date)}'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_paid_message(to_number, amount):
        msg = f'Your balance of R{amount} has been paid in full to Dimofusion'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_close_message(to_number, first_name, last_name):
        msg = f'Hi {first_name} {last_name}, your account at Dimofusion has been closed'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_balance_due_soon_message(to_number, full_name, total, due_date):
        msg = f'Hi {full_name}, your balance of R{total} from Dimofusion is due on {format_date(due_date)}'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_balance_due_warning_message(to_number, full_name, total, due_date):
        msg = f'Hi {full_name}, this is a WARNING that your balance of R{total} is due today: {format_date(due_date)}'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_past_due_message(to_number, full_name, total, due_date):
        msg = f'Hi {full_name}, your balance is past due: {format_date(due_date)}. Your total of R{total} ' \
              f'has accrued an additional 25% interest and your new total is: R{apply_interest(total)}'
        WhatsAppClient.send_message(msg, to_number)
