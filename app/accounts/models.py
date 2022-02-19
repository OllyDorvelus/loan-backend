from django.db import models
from app.users.models import AbstractModel
from djmoney.models.fields import MoneyField


class AccountBase(AbstractModel):
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='ZA')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='accounts')

    class Meta:
        abstract = True


class LoanAccount(AccountBase):
    due_date = models.DateField()
