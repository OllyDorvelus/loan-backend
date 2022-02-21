from django.db import models
from app.users.models import AbstractModel
from djmoney.models.fields import MoneyField
from moneyed import ZAR
from django.db.models.signals import pre_save, post_save
from app.api.whats_app_client import WhatsAppClient
from datetime import date
from django.db import transaction as trans

LOAN_STATUS = (
    ('ACTIVE', 'active'),
    ('PAST_DUE', 'past_due'),
    ('PENDING', 'pending'),
    ('PAID', 'paid'),
    ('CLOSED', 'closed'),
)


# managers
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


class TransactionManager(models.Manager):
    def create_transaction(self, account, amount, **extra_fields):
        if not account:
            raise ValueError("Transaction must have account")
        if not amount:
            raise ValueError("Transaction must have amount")
        transaction = self.model(account=account, amount=amount, **extra_fields)
        transaction.save(using=self._db)
        return transaction


class AccountBase(AbstractModel):
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency=ZAR)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='accounts')
    accepted_date = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True


class LoanAccount(AccountBase):
    due_date = models.DateField()
    status = models.CharField(max_length=14, choices=LOAN_STATUS, default='PENDING')
    interest_rate = models.DecimalField(max_digits=2, decimal_places=2, default=0.25)
    objects = AccountManager()

    def __str__(self):
        return f'{self.user.email} - {self.balance} - {self.status}'

    def accept(self):
        self.status = 'ACTIVE'
        self.accepted_date = date.today()
        self.save()
        return self

    def close(self):
        self.status = 'CLOSED'
        self.save()
        return self

    def add(self, amount):
        with trans.atomic():
            Transaction.objects.create(self, amount)
            self.balance.amount += amount
            self.save()

    def subtract(self, amount):
        with trans.atomic():
            Transaction.objects.create(self, amount * -1)
            self.balance.amount -= amount
            self.save()

    @property
    def principal(self):
        return self.balance.amount

    @property
    def total(self):
        return (self.principal * self.interest_rate) + self.principal


class Transaction(AbstractModel):
    amount = MoneyField(max_digits=10, decimal_places=2, default_currency=ZAR)
    account = models.ForeignKey('accounts.LoanAccount', on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f'{self.account.user.last_name} - {self.account.balance} - {self.created}'


# signals
def send_message_when_pending_to_active(sender, instance, **kwargs):
    if instance.id:
        old_instance = LoanAccount.objects.get(pk=instance.id)
        instance.accepted_date = date.today()
        if old_instance.status.lower() == 'pending' and instance.status.lower() == 'active':
            WhatsAppClient.send_accept_loan_message(instance.user.customer.whatsapp_number, instance.user.first_name,
                                                    instance.user.last_name, instance.balance, instance.due_date,
                                                    instance.accepted_date)
        if instance.amount <= 0:
            instance.status = 'PAID'
            WhatsAppClient.send_paid_message(instance.user.customer.whatsapp_number, old_instance.total)


def send_welcome_message(sender, instance, **kwargs):
    if instance.created:
        WhatsAppClient.send_welcome_message(instance.user.customer.whatsapp_number, instance.user.first_name,
                                            instance.user.last_name, instance.principal)

    if instance.status.lower() == 'closed':
        WhatsAppClient.send_close_message(instance.user.customer.whatsapp_number, instance.user.first_name, instance.user.last_name)


pre_save.connect(send_message_when_pending_to_active, sender=LoanAccount)
post_save.connect(send_welcome_message, sender=LoanAccount)
