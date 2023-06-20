from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import ActionLineOrderItem


@receiver(post_save, sender=ActionLineOrderItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update action total on lineitem update/create
    """
    instance.action.update_total()


@receiver(post_delete, sender=ActionLineOrderItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update action total on lineitem delete
    """
    instance.action.update_total()
