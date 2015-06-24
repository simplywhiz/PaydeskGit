from django.contrib import admin
from payment.models import PaymentType, TransactionSummary, TransactionSummaryDetail


class TransactionSummaryDetailInline(admin.TabularInline):
    model = TransactionSummaryDetail
    extra = 0

class TransactionSummaryAdmin(admin.ModelAdmin):
    list_display = ['total_amount', 'transaction_ref', 'payment_method', 'phone_number', 'user', 'date_of_transaction']
    list_filter = ['date_of_transaction', 'payment_method']
    search_fields = []
    inlines = [ TransactionSummaryDetailInline ]


class TransactionSummaryDetailAdmin(admin.ModelAdmin):
    list_display = ['payment_type', 'amount']
    list_filter = ['payment_type']

admin.site.register(PaymentType)
admin.site.register(TransactionSummary, TransactionSummaryAdmin)
admin.site.register(TransactionSummaryDetail, TransactionSummaryDetailAdmin)

# Register your models here.
