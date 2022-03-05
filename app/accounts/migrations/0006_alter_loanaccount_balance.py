# Generated by Django 3.2 on 2022-03-05 22:48

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_loanaccount_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanaccount',
            name='balance',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('0.0'), default_currency='ZAR', max_digits=10),
        ),
    ]