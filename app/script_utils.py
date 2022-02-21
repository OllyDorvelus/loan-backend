from app.accounts.models import LoanAccount
from datetime import date, timedelta
from app.api.whats_app_client import WhatsAppClient


def send_balance_due_soon_notification():
    two_days_from_now = date.today() + timedelta(days=2)
    accounts = LoanAccount.objects.filter(status='ACTIVE', balance__amount__gt=0,
                                          due_date=two_days_from_now).select_related('user')
    for account in accounts:
        WhatsAppClient.send_balance_due_soon_message(account.user.whatsapp_number,
                                                     account.user.full_name, account.total,
                                                     account.due_date)
        print(f'Sent notification to Customer: {account.user.full_name}')


def send_balance_due_warning_today_notification():
    today = date.today()
    accounts = LoanAccount.objects.filter(status='ACTIVE', balance__amount__gt=0,
                                          due_date=today).select_related('user')
    for account in accounts:
        WhatsAppClient.send_balance_due_warning_message(account.user.whatsapp_number, account.user.full_name,
                                                        account.total, account.due_date)
        print(f'Sent notification to Customer: {account.user.full_name}')


def send_balance_past_due_notification():
    today = date.today()
    accounts = LoanAccount.objects.filter(status='ACTIVE', balance__amount__gt=0).select_related('user')

    for account in accounts:
        WhatsAppClient.send_past_due_message(account.user.whatsapp_number, account.user.full_name,
                                             account.total, account.due_date)
        if (today - account.due_date).days >= 2:
            account.status = 'PAST_DUE'
            account.save()
            print(f'Sent notification to Customer: {account.user.full_name}')
