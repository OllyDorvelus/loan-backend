from app.accounts.models import LoanAccount
from datetime import date, timedelta
from app.api.whats_app_client import WhatsAppClient


def send_balance_due_soon_notification():
    two_days_from_now = date.today() + timedelta(days=2)
    accounts = LoanAccount.objects.filter(status=LoanAccount.ACTIVE, balance__gt=0,
                                          due_date=two_days_from_now).select_related('user')
    msg_out = 0
    for account in accounts:
        WhatsAppClient.send_balance_due_soon_message(account.user.whatsapp_number,
                                                     account.user.full_name, account.balance.amount,
                                                     account.due_date)
        msg_out += 1
        print(f'Sent notification to Customer: {account.user.full_name}')
    print(f'Total messages sent for balance due soon: {msg_out}')


def send_balance_due_warning_today_notification():
    today = date.today()
    accounts = LoanAccount.objects.filter(status=LoanAccount.ACTIVE, balance__gt=0,
                                          due_date=today).select_related('user')
    msg_out = 0
    for account in accounts:
        WhatsAppClient.send_balance_due_warning_message(account.user.whatsapp_number, account.user.full_name,
                                                        account.total, account.due_date)
        print(f'Sent notification to Customer: {account.user.full_name}')
        msg_out += 1
    print(f'Total messages sent for balance warning: {msg_out}')


def send_balance_past_due_notification():
    today = date.today()
    accounts = LoanAccount.objects.filter(status=LoanAccount.ACTIVE, balance__gt=0).select_related('user')
    msg_out = 0
    for account in accounts:
        WhatsAppClient.send_past_due_message(account.user.whatsapp_number, account.user.full_name,
                                             account.total, account.due_date)
        if (today - account.due_date).days >= 2:
            account.status = LoanAccount.PAST_DUE
            account.apply_interest()
            print(f'Sent notification to Customer: {account.user.full_name}')
            msg_out += 1
    print(f'Total messages sent for balance past due: {msg_out}')
