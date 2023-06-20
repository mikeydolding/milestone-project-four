import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from items.models import Item


class Action(models.Model):
    action_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    action_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def _generate_action_number(self):
        """
        Generate a random, unique action number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.action_total = self.lineorderitems.aggregate(Sum('lineorderitem_total'))['lineorderitem_total__sum']
        if self.action_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.action_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.action_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the action number
        if it hasn't been set already.
        """
        if not self.action_number:
            self.action_number = self._generate_action_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.action_number


class ActionLineOrderItem(models.Model):
    action = models.ForeignKey(Action, null=False, blank=False, on_delete=models.CASCADE, related_name='lineorderitems')
    item = models.ForeignKey(Item, null=False, blank=False, on_delete=models.CASCADE)
    item_size = models.CharField(max_length=2, null=True, blank=True) # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineorderitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineorderitem total
        and update the action total.
        """
        self.lineorderitem_total = self.item.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.item.sku} on action {self.action.action_number}'