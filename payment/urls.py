from django.conf.urls import url
from .views import receive_payment, payment_gateway, gateway_reply
from django.contrib import admin

admin.site.site_header = 'Paydesk Administration'

urlpatterns = [
    url(r'^process/$', receive_payment, name='receive_payment'),
    url(r'^gateway/$', payment_gateway, name='payment_gateway'),
    url(r'^reply/$', gateway_reply, name='gateway_reply'),
]