import os
from datetime import date
from twilio.rest import Client
from app.utils import format_date, apply_interest, format_money

account_sid = os.getenv('WA_ACCOUNT_SID')
auth_token = os.getenv('WA_AUTH_TOKEN')
FROM_NUMBER = os.getenv('WA_FROM_NUMBER')
client = Client(account_sid, auth_token)
SHOULD_SEND_MESSAGE_TO_WHATSAPP = False


class WhatsAppClient:

    @staticmethod
    def send_message(msg, to_number):
        if SHOULD_SEND_MESSAGE_TO_WHATSAPP:
            client.messages.create(
                body=msg,
                from_=FROM_NUMBER,
                to=to_number
            )
        else:
            print(f'\n{to_number}: {msg}\n')

    @staticmethod
    def send_balance_change_message(to_number, full_name, prev_amount, new_amount):
        msg = f'Hi {full_name}, your balance at Dimofusion has changed from {format_money(prev_amount)} to {format_money(new_amount)}'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_submitted_application_message(to_number, full_name, amount):
        msg = f'Hi {full_name}, on {format_date(date.today())}, your loan application for {format_money(amount)} ' \
              f'Dimofusion and we will notify you on the status of your application. ' \
              f'We will let you know the interest rate and total due when your application is submitted'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_accept_loan_message(to_number, full_name, balance, due_date, total):
        msg = f'Hi {full_name} you have taken out a loan of R{balance}' \
              f'with Dimofusion at a 25% interest rate. The total debt payable on  {format_date(due_date)} is ' \
              f'{format_money(total)}'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_paid_message(to_number, amount):
        msg = f'Your balance of {format_money(amount)} has been paid in full to Dimofusion'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_close_message(to_number, first_name, last_name):
        msg = f'Hi {first_name} {last_name}, your account at Dimofusion has been closed'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_balance_due_soon_message(to_number, full_name, total, due_date):
        msg = f'Hi {full_name}, your balance of R{total} from Dimofusion is due in two days on {format_date(due_date)}'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_balance_due_warning_message(to_number, full_name, total, due_date):
        msg = f'Hi {full_name}, this is a WARNING that your balance of {format_money(total)} is due today: {format_date(due_date)}'
        WhatsAppClient.send_message(msg, to_number)

    @staticmethod
    def send_past_due_message(to_number, full_name, total, due_date):
        msg = f'Hi {full_name}, your balance is past due: {format_date(due_date)}. Your total of R{total} ' \
              f'has accrued an additional 25% interest and your new total is: R{apply_interest(total)}'
        WhatsAppClient.send_message(msg, to_number)
