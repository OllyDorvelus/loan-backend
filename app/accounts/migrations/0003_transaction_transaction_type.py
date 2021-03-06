# Generated by Django 3.2 on 2022-02-26 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="transaction_type",
            field=models.CharField(
                choices=[("ADDED", "added"), ("DEDUCTED", "deducted")],
                default="ADDED",
                max_length=10,
            ),
            preserve_default=False,
        ),
    ]
