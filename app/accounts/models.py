from django.db import models, transaction as trans
from app.users.models import AbstractModel
from djmoney.models.fields import MoneyField
from moneyed import ZAR
from django.db.models.signals import pre_save, post_save
from app.api.whats_app_client import WhatsAppClient
from datetime import date
from django.core.validators import RegexValidator


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
    def create_transaction(self, account, amount, transaction_type, **extra_fields):
        if not account:
            raise ValueError("Transaction must have account")
        if not amount:
            raise ValueError("Transaction must have amount")
        if not transaction_type:
            raise ValueError("Transaction must have transaction type")
        transaction = self.model(account=account, amount=amount, transaction_type=transaction_type, **extra_fields)
        transaction.save(using=self._db)
        return transaction


class AccountBase(AbstractModel):
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency=ZAR)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='accounts')
    accepted_date = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True


class LoanAccount(AccountBase):
    ACTIVE = 'active'
    PAST_DUE = 'past_due'
    PENDING = 'pending'
    PAID = 'paid'
    CLOSED = 'closed'
    LOAN_STATUS = (
        (ACTIVE, 'active'),
        (PAST_DUE, 'past_due'),
        (PENDING, 'pending'),
        (PAID, 'paid'),
        (CLOSED, 'closed'),
    )

    principal = MoneyField(max_digits=10, decimal_places=2, default_currency=ZAR)
    due_date = models.DateField()
    status = models.CharField(max_length=14, choices=LOAN_STATUS, default='PENDING')
    interest_rate = models.DecimalField(max_digits=2, decimal_places=2, default=0.25)
    objects = AccountManager()

    def __str__(self):
        return f'{self.user.email} - {self.balance} - {self.status}'

    def accept(self):
        if self.status == self.PENDING:
            with trans.atomic():
                self.status = self.ACTIVE
                self.accepted_date = date.today()
                self.balance = (self.balance.amount * self.interest_rate) + self.principal.amount
            WhatsAppClient.send_accept_loan_message(self.user.whatsapp_number, self.user.full_name,
                                                    self.due_date, self.balance.amount)

            return self

    def close(self):
        self.status = self.CLOSED
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
    def total(self):
        return self.balance.amount

    def __str__(self):
        return f'{self.user.full_name} - {self.balance.amount}'


class Transaction(AbstractModel):
    ADDED = 'ADDED'
    DEDUCTED = 'DEDUCTED'
    TRANSACTION_TYPE = (
        (ADDED, 'added'),
        (DEDUCTED, 'deducted')
    )
    amount = MoneyField(max_digits=10, decimal_places=2, default_currency=ZAR)
    account = models.ForeignKey('accounts.LoanAccount', on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=10)

    objects = TransactionManager()

    def __str__(self):
        return f'{self.account.user.full_name} - {self.amount} - {self.created}'


class BankName(AbstractModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BankType(AbstractModel):
    CHEQUE = 'CHEQUE'
    SAVINGS = 'SAVINGS'
    ACCOUNT_TYPE = (
        (CHEQUE, 'cheque'),
        (SAVINGS, 'savings'),
    )
    type = models.CharField(max_length=10, choices=ACCOUNT_TYPE)

    def __str__(self):
        return f'{self.type}'


class Bank(AbstractModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    bank_name = models.ForeignKey('accounts.BankName', on_delete=models.CASCADE)
    bank_type = models.ForeignKey('accounts.BankType', on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20,
                                      validators=[RegexValidator('^[0-9]+$',
                                                                 message='Account must be numeric digits',
                                                                 code='invalid_account')]
                                      )

    def __str__(self):
        return f'{self.user.full_name} - {self.bank_name} - {self.account_number}'


# signals
def send_message_when_pending_to_active(sender, instance, **kwargs):
    if instance.id:
        old_instance = LoanAccount.objects.get(pk=instance.id)
        instance.accepted_date = date.today()
        if old_instance.status.lower() == 'pending' and instance.status.lower() == 'active':
            instance.accept()


def send_message_when_balance_becomes_zero(sender, instance, **kwargs):
    if instance.balance.amount <= 0 and instance.id:
        old_instance = LoanAccount.objects.get(pk=instance.id)
        instance.status = 'PAID'
        WhatsAppClient.send_paid_message(instance.user.customer.whatsapp_number, old_instance.balance.amount)


def send_submitted_application_message(sender, instance, **kwargs):
    if instance.created:
        WhatsAppClient.send_submitted_application_message(instance.user.customer.whatsapp_number,
                                                          instance.user.full_name,
                                                          instance.principal)


def send_close_message_on_status_change(sender, instance, **kwargs):
    if instance.status.lower() == 'closed':
        WhatsAppClient.send_close_message(instance.user.customer.whatsapp_number, instance.user.first_name,
                                          instance.user.last_name)


def send_balance_change_message(sender, instance, **kwargs):
    if instance.id:
        old_instance = LoanAccount.objects.get(pk=instance.id)
        old_amount = old_instance.balance.amount
        new_amount = instance.balance.amount
        if old_amount != new_amount:
            WhatsAppClient.send_submitted_application_message(instance.user.whatsapp_number, instance.user.full_name,
                                                              old_amount, new_amount)
            new_transaction = {'amount': old_amount - new_amount, 'account': instance}
            if new_amount > old_amount:
                new_transaction['transaction_type'] = Transaction.ADDED
            else:
                new_transaction['transaction_type'] = Transaction.DEDUCTED
            Transaction.objects.create_transaction(**new_transaction)


pre_save.connect(send_message_when_pending_to_active, sender=LoanAccount)
pre_save.connect(send_message_when_balance_becomes_zero, sender=LoanAccount)
pre_save.connect(send_balance_change_message, sender=LoanAccount)
post_save.connect(send_submitted_application_message, sender=LoanAccount)
post_save.connect(send_close_message_on_status_change, sender=LoanAccount)
