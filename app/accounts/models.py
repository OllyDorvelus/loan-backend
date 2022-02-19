from django.db import models
from app.users.models import AbstractModel
from djmoney.models.fields import MoneyField


LOAN_STATUS = (
    ('ACTIVE', 'active'),
    ('PAST_DUE', 'past_due'),
    ('PENDING', 'pending'),
    ('PAID', 'paid'),
    ('CLOSED', 'closed'),
)


class AccountBase(AbstractModel):
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='ZA', unique=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='accounts')

    class Meta:
        abstract = True


class LoanAccount(AccountBase):
    due_date = models.DateField()
    status = models.CharField(max_length=14, choices=LOAN_STATUS, default='PENDING')

    def __str__(self):
        return f'{self.user.email} - {self.balance} - {self.status}'
