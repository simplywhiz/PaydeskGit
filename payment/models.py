from django.contrib.auth.models import User
from django.db import models


PAYMENT_METHOD = (
    ('CC', 'CREDIT CARD'),
    ('DC', 'DEBIT CARD'),
    ('GC', 'GIFT CARD'),
    ('PP', 'PAY PAL'),
)


class PaymentType(models.Model):
    name = models.CharField(max_length=20, help_text='Enter short descriptive name of the payment to be shown to user. ex. "Tithe"')
    show_to_user = models.BooleanField(default=True, help_text='Select true or false to show this option on the front end.')

    def __str__(self):
        return self.name
# Create your models here.


class TransactionSummary(models.Model):
    user = models.ForeignKey(User, null=True, help_text='User that initiated the transaction. set to Null if the user is a guest.')
    transaction_ref = models.CharField(max_length=100, help_text='Transaction id returned form the payment gateway.')
    payment_method = models.CharField(max_length=3, choices=PAYMENT_METHOD, help_text='The payment method for the transaction.')
    phone_number = models.CharField(max_length=15, null=True, help_text='Save the phone number entered by anonymous users')
    # add other details from the transaction gateway like payment SUCCESS etc
    total_amount = models.DecimalField(max_digits=20, decimal_places=4, help_text='Total amount for the particular transaction sent to the payment gateway.')
    date_of_transaction = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.total_amount)


# Retrieve history of transaction with the "user" and group by the "transaction_id" for summary to the user
# NOTE THIS TABLE IS ONLY UPDATED IF THE PAYMENT WAS SUCCESSFUL
class TransactionSummaryDetail(models.Model):
    transaction_summary = models.ForeignKey(TransactionSummary)
    payment_type = models.ForeignKey(PaymentType)
    amount = models.DecimalField(max_digits=20, decimal_places=4, help_text='Amount paid for each payment type.')
