from datetime import date
from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import PaymentType, PAYMENT_METHOD, TransactionSummary, TransactionSummaryDetail
from .forms import PaymentGatewayForm, PaymentForm


# method to generate PaymentForm
def payment_form(pay_options_queryset):
    # dynamically build all payment form fields with the pay_options_queryset and other fields
    fields = {}
    for option in pay_options_queryset:
        fields[option.name] = forms.DecimalField(max_digits=20, decimal_places=4, min_value=0, required=False,
                                                 widget=forms.NumberInput(attrs={'class': 'payment_field form-control', 'placeholder': '0.00'}))
    return type('PaymentForm', (forms.Form,), fields)


def receive_payment(request):
    # select all fields marked by the admin to be shown to users
    pay_options = PaymentType.objects.filter(show_to_user=True)
    if request.method == 'POST':
        new_form = payment_form(pay_options)
        # collect dynamically generated form and other form fields
        form = new_form(request.POST)
        other_form_fields = PaymentForm(request.POST)

        if form.is_valid() and other_form_fields.is_valid():
            # variable to hold total value of all transaction sent from the client
            total_value = 0
            # Dictionary to hold a summary of the transaction to persist in the session
            transaction_summary = {}
            # Dictionary to hold all relevant(non-zero payment fields) transaction to persist in the session
            transaction_summary_detail = {}

            payment_method = other_form_fields.cleaned_data['payment_method']
            transaction_summary['payment_method'] = payment_method
            transaction_summary['phone_number'] = other_form_fields.cleaned_data['phone_number']
            # loop through to get all relevant(non-zero payment) fields entered by the user
            for option in pay_options:
                value = form.cleaned_data[option.name]
                if value is not None and value > 0:
                    transaction_summary_detail[option.name] = float(value)
                    total_value += value

            # if no amount was entered(total payment is zero) go back to the payment page
            if total_value == 0:
                messages.info(request, 'You have not filled out any payment options, please use the fields provided below.', extra_tags='alert alert-info alert-dismissible')
                return render(request, 'payment/receive_payment.html', {'form': form, 'other_form_fields': other_form_fields})

            # ensure value being sent to the payment gateway is what was shown to the user and save all in session
            if total_value == other_form_fields.cleaned_data['total_payment']:
                transaction_summary['total_payment'] = float(total_value)
                request.session['transaction_summary'] = transaction_summary
                request.session['transaction_summary_detail'] = transaction_summary_detail
                messages.info(request, 'Checked out nicely '+str(total_value), extra_tags='alert alert-info alert-dismissible')
            # Route data to the appropriate gateway based on selected payment method
            if payment_method=='CC':
                # Route to card processing gateway
                pass
            elif payment_method=='DC':
                # Route to card processing gateway
                pass
            elif payment_method=='GC':
                # process using Gift Card
                pass
            elif payment_method=='PP':
                # Route to Pay pal
                pass

            """ For test purposes only. redirect to dummy card details page."""
            return redirect('payment:payment_gateway')
    else:
        form = payment_form(pay_options)
        if request.user.is_authenticated():
            other_form_fields = PaymentForm(initial={'phone_number': request.user.username})
        else:
            other_form_fields = PaymentForm()
    return render(request, 'payment/receive_payment.html', {'form': form, 'other_form_fields': other_form_fields})


def payment_gateway(request):
    if request.method == 'POST':
        form = PaymentGatewayForm(request.POST, prefix='pgf')
        if form.is_valid():
            """ For test purposes only. redirect to gateway reply page """
            # save reply to database
            return redirect('payment:gateway_reply')
    else:
        form = PaymentGatewayForm(prefix='pgf')
    return render(request, 'payment/payment_gateway.html', {'form': form})


def gateway_reply(request):
    """ Save transaction summary in the database """
    transaction_summary = request.session['transaction_summary']
    tx_summary = TransactionSummary()
    tx_summary.total_amount = transaction_summary['total_payment']
    tx_summary.payment_method = transaction_summary['payment_method']
    tx_summary.phone_number = transaction_summary['phone_number']
    tx_summary.date_of_transaction = date.today()
    tx_summary.transaction_ref = '123e439926ejnfjhk'
    if request.user.is_authenticated():
        tx_summary.user=request.user
    tx_summary.save()

    """ save detail of each transaction in the database as well attached to the particular transaction """
    transaction_summary_detail = request.session['transaction_summary_detail']
    for key in transaction_summary_detail:
        tx_summary_detail = TransactionSummaryDetail()
        tx_summary_detail.amount = transaction_summary_detail[key]
        tx_summary_detail.payment_type = PaymentType.objects.get(name=key)
        tx_summary_detail.transaction_summary = tx_summary
        tx_summary_detail.save()

    return render(request, 'payment/gateway_reply.html', {'tx_summary':tx_summary})