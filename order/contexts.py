from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from items.models import Item


def order_contents(request):

    order_items = []
    total = 0
    product_count = 0
    order = request.session.get('order', {})

    for order_item_id, order_item_data in order.items():
        if isinstance(order_item_data, int):
            item = get_object_or_404(Item, pk=order_item_id)
            total += order_item_data * item.price
            product_count += order_item_data
            order_items.append({
                'order_item_id': order_item_id,
                'quantity': order_item_data,
                'item': item,
            })
        else:
            item = get_object_or_404(Item, pk=order_item_id)
            for size, quantity in order_item_data['order_items_by_size'].order_items():
                total += quantity * item.price
                product_count += quantity
                order_items.append({
                    'order_item_id': order_item_id, 
                    'quantity': order_item_data,
                    'item': item,
                    'size': size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'order_items': order_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
