# Generated by Django 3.2 on 2022-02-21 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanaccount',
            name='interest_rate',
            field=models.DecimalField(decimal_places=2, default=0.25, max_digits=2),
        ),
    ]