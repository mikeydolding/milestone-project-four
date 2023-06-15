from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from items.models import Item


def order_contents(request):

    orderItems = []
    total = 0
    product_count = 0
    order = request.session.get('order', {})

    for orderItem_id, orderItem_data in order.items():
        if isinstance(orderItem_data, int):
            item = get_object_or_404(Item, pk=orderItem_id)
            total += orderItem_data * item.price
            product_count += orderItem_data
            orderItems.append({
                'orderItem_id': orderItem_id,
                'quantity': orderItem_data,
                'item': item,
            })
        else:
            item = get_object_or_404(Item, pk=orderItem_id)
            for size, quantity in orderItem_data['orderItems_by_size'].orderItems():
                total += quantity * item.price
                product_count += quantity
                orderItems.append({
                    'orderItem_id': orderItem_id, 
                    'quantity': orderItem_data,
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
        'orderItems': orderItems,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
