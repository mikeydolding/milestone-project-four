from django.contrib import admin
from .models import Action, ActionLineOrderItem
 
# Register your models here.


class ActionLineOrderItemAdminInline(admin.TabularInline):
    model = ActionLineOrderItem
    readonly_fields = ("lineorderitem_total",)


class ActionAdmin(admin.ModelAdmin):
    inlines = (ActionLineOrderItemAdminInline,)

    readonly_fields = (
        "action_number",
        "date",
        "delivery_cost",
        "action_total",
        "grand_total",
        #"original_bag",
        #"stripe_pid",
    )

    fields = (
        "action_number",
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
        "action_total",
        "grand_total",
        #"original_bag",
        #"stripe_pid",
    )

    list_display = (
        "action_number",
        "date",
        "full_name",
        "action_total",
        "delivery_cost",
        "grand_total",
    )

    ordering = ("-date",)


admin.site.register(Action, ActionAdmin)
