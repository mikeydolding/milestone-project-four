from django.contrib import admin
from .models import Transaction, TransactionLineOrderItem
 
# Register your models here.


class TransactionLineOrderItemAdminInline(admin.TabularInline):
    model = TransactionLineOrderItem
    readonly_fields = ("lineorderitem_total",)


class TransactionAdmin(admin.ModelAdmin):
    inlines = (TransactionLineOrderItemAdminInline,)

    readonly_fields = (
        "transaction_number",
        "date",
        "delivery_cost",
        "transaction_total",
        "grand_total",
        #"original_bag",
        #"stripe_pid",
    )

    fields = (
        "transaction_number",
        #"user_profile",
        "date",
        "full_name",
        "email",
        "phone_number",
        "country",
        "postcode",
        "town_or_city",
        "street_address1",
        "street_address2",
        "county",
        "delivery_cost",
        "transaction_total",
        "grand_total",
        #"original_bag",
        #"stripe_pid",
    )

    list_display = (
        "transaction_number",
        "date",
        "full_name",
        "transaction_total",
        "delivery_cost",
        "grand_total",
    )

    ordering = ("-date",)


admin.site.register(Transaction, TransactionAdmin)
