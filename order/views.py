from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404

from django.contrib import messages

from items.models import Item

# Create your views here.

def view_order(request):
    """ A view that renders the order contents page """

    return render(request, 'order/order.html')

def add_to_order(request, order_item_id):
    """ Add a quantity of the specified item to the shopping order """

    item = get_object_or_404(Item, pk=order_item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'item_size' in request.POST:  
        size = request.POST['item_size']
        print('size',request.POST['item_size'])
    order = request.session.get('order', {})

    if size:
        if order_item_id in list(order.keys()):
            if size in order[order_item_id]['order_items_by_size'].keys():
                order[order_item_id]['order_items_by_size'][size] += quantity
                messages.success(request, 
                                    (f'Updated size {size.upper()} '
                                     f'{item.name} quantity to '
                                     f'{order[order_item_id]["order_items_by_size"][size]}'))
            else:
                order[order_item_id]['order_items_by_size'][size] = quantity
                messages.success(request,
                                 (f'Added size {size.upper()} '
                                  f'{item.name} to your order'))
        else:
            order[order_item_id] = {'order_items_by_size': {size: quantity}}
            messages.success(request,
                             (f'Added size {size.upper()} '
                              f'{item.name} to your order'))
    else:
        if order_item_id in list(order.keys()):
            order[order_item_id] += quantity
            messages.success(request,
                             (f'Updated {item.name} '
                              f'quantity to {order[order_item_id]}'))
        else:
            order[order_item_id] = quantity
            messages.success(request, f'Added {item.name} to your order')

    request.session['order'] = order
    #print(request.session['order'])
    return redirect(redirect_url)
    
def update_order(request, order_item_id):
    """ Update quantity of the specified item to the shopping order """

    item = get_object_or_404(Item, pk=order_item_id)
    quantity = int(request.POST.get('quantity'))
    size = None   
    if 'item_size' in request.POST:  
        size = request.POST['item_size']
        print('size',request.POST['item_size'])
    order = request.session.get('order', {})

    if size:
        if quantity > 0:
            order[order_item_id]['order_items_by_size'][size] = quantity
            messages.success(request,
                             (f'Updated size {size.upper()} '
                              f'{item.name} quantity to '
                              f'{order[order_item_id]["order_items_by_size"][size]}'))

        else:
            del order[order_item_id]['order_items_by_size'][size]
            if not order[order_item_id]['order_items_by_size']:
                order.pop(order_item_id)
            messages.success(request,
                             (f'Removed size {size.upper()} '
                              f'{item.name} from your order'))

    else:
        if quantity > 0:
            order[order_item_id] = quantity  
            messages.success(request,
                             (f'Updated {item.name} '
                              f'quantity to {order[order_item_id]}'))

        else:
            order.pop(order_item_id)
            messages.success(request,
                             (f'Removed {item.name} '
                              f'from your order'))

    request.session['order'] = order
    return redirect(reverse('view_order'))

def remove_from_order(request, order_item_id):
    """Remove the item from the shopping order"""
    #print('request data',request.POST)
    #print('order_item_id',order_item_id)

    try:
        item = get_object_or_404(Item, pk=order_item_id)
        size = None
        if 'item_size' in request.POST:
            size = request.POST['item_size']
        order = request.session.get('order', {})
        #print('item_size in request.POST',order)

        if size:
            #print('size',order[order_item_id]['order_items_by_size'][size])
            del order[order_item_id]['order_items_by_size'][size]
            if not order[order_item_id]['order_items_by_size']:
                order.pop(order_item_id)
                messages.success(request, 
                                    (f'Removed size {size.upper()} '
                                     f'{item.name} quantity to '))
        else:
            order.pop(order_item_id)
            messages.success(request, f'Removed {item.name} from your order')

        request.session['order'] = order
        return HttpResponse(status=200)
 
    except Exception as e:
        return HttpResponse(status=500)