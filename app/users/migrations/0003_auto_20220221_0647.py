# Generated by Django 3.2 on 2022-02-21 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customer_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='id_file',
            field=models.FileField(blank=True, upload_to='uploads/ids'),
        ),
        migrations.AddField(
            model_name='customer',
            name='payslip',
            field=models.FileField(blank=True, upload_to='uploads/payslips'),
        ),
    ]
