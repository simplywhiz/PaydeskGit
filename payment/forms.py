from django import forms
from .models import PAYMENT_METHOD


class PaymentGatewayForm(forms.Form):
    name_on_card = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'class':'form-control'}))
    card_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    cvv = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class':'form-control'}))
    date_of_expiry = forms.DateField()



class PaymentForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD, widget=forms.RadioSelect(attrs={'class': 'form-control'}))
    total_payment = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'total_payment',
                                                                       'readonly': True, 'placeholder': '0.00'}))