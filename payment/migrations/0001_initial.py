# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(help_text='Enter short descriptive name of the payment to be shown to user. ex. "Tithe"', max_length=20)),
                ('show_to_user', models.BooleanField(default=True, help_text='Select true or false to show this option on the front end.')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionSummary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('transaction_ref', models.CharField(help_text='Transaction id returned form the payment gateway.', max_length=100)),
                ('payment_method', models.CharField(choices=[('CC', 'CREDIT CARD'), ('DC', 'DEBIT CARD'), ('GC', 'GIFT CARD'), ('PP', 'PAY PAL')], help_text='The payment method for the transaction.', max_length=3)),
                ('phone_number', models.CharField(null=True, help_text='Save the phone number entered by anonymous users', max_length=15)),
                ('total_amount', models.DecimalField(decimal_places=4, max_digits=20, help_text='Total amount for the particular transaction sent to the payment gateway.')),
                ('date_of_transaction', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, help_text='User that initiated the transaction. set to Null if the user is a guest.')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionSummaryDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=4, max_digits=20, help_text='Amount paid for each payment type.')),
                ('payment_type', models.ForeignKey(to='payment.PaymentType')),
                ('transaction_summary', models.ForeignKey(to='payment.TransactionSummary')),
            ],
        ),
    ]
