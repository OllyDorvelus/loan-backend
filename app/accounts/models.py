from django.db import models
from app.users.models import AbstractModel
from djmoney.models.fields import MoneyField
from moneyed import ZAR
from django.db.models.signals import pre_save
from app.api.whats_app_client import WhatsAppClient
from datetime import date

LOAN_STATUS = (
    ('ACTIVE', 'active'),
    ('PAST_DUE', 'past_due'),
    ('PENDING', 'pending'),
    ('PAID', 'paid'),
    ('CLOSED', 'closed'),
)


class AccountManager(models.Manager):

    def create_loan_account(self, user, balance, due_date, status='pending', **extra_fields):
        if not user:
            raise ValueError("Account must have user.")

        if not balance:
            raise ValueError("Account must have balance.")

        if not due_date:
            raise ValueError("Account must have a due date.")

        account = self.model(user=user, balance=balance, due_date=due_date, status=status, **extra_fields)
        account.save(using=self._db)
        return account


class AccountBase(AbstractModel):
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency=ZAR)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='accounts')
    accepted_date = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True


class LoanAccount(AccountBase):
    due_date = models.DateField()
    status = models.CharField(max_length=14, choices=LOAN_STATUS, default='PENDING')

    objects = AccountManager()

    def __str__(self):
        return f'{self.user.email} - {self.balance} - {self.status}'

    def accept(self):
        self.active = True
        self.save()
        self.refresh_from_db()
        return self


# signals

def send_message_when_pending_to_active(sender, instance, **kwargs):
    if instance.id:
        old_instance = LoanAccount.objects.get(pk=instance.id)
        instance.accepted_date = date.today()
        if old_instance.status.lower() == 'pending' and instance.status.lower() == 'active':
            WhatsAppClient.send_accept_notice(instance.user.customer.whatsapp_number, instance.user.first_name,
                                              instance.user.last_name, instance.balance, instance.due_date,
                                              instance.accepted_date)


pre_save.connect(send_message_when_pending_to_active, sender=LoanAccount)

