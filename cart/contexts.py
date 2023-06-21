from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from items.models import Item

def cart_contents(request):

    cart_items = []
    total = 0
    item_count = 0
    cart = request.session.get('cart', {})

    #for cart_item_id, quantity in cart.items():
    #    item = get_object_or_404(Item, pk=cart_item_id)
    #    total += quantity * item.price
    #    item_count += quantity
    #    cart_items.append({
    #        'cart_item_id': cart_item_id,
    #        'quantity': quantity,
    #        'item': item,
    #    })
    for cart_item_id, cart_item_data in cart.items():
        if isinstance(cart_item_data, int):
            item = get_object_or_404(Item, pk=cart_item_id)
            total += cart_item_data * item.price
            item_count += cart_item_data
            cart_items.append({
                'cart_item_id': cart_item_id,
                'quantity': cart_item_data,
                'item': item,
            })
        else:
            item = get_object_or_404(Item, pk=cart_item_id)
            for size, quantity in cart_item_data['cart_items_by_size'].items():
                total += quantity * item.price
                item_count += quantity
                cart_items.append({
                    'cart_item_id': cart_item_id,
                    'quantity': quantity,
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
        'cart_items': cart_items,
        'total': total,
        'item_count': item_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context