from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import TransactionLineCartItem


@receiver(post_save, sender=TransactionLineCartItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update transaction total on lineitem update/create
    """
    instance.transaction.update_total()


@receiver(post_delete, sender=TransactionLineCartItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update transaction total on lineitem delete
    """
    instance.transaction.update_total()
