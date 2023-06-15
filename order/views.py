from django.shortcuts import render, redirect

# Create your views here.

def view_order(request):
    """ A view that renders the order contents page """

    return render(request, 'order/order.html')

def add_to_order(request, order_item_id):
    """ Add a quantity of the specified product to the shopping order """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'order_item_size' in request.POST:
        size = request.POST['order_item_size']
    order = request.session.get('order', {})

    if size:
        if order_item_id in list(order.keys()):
            if size in order[order_item_id]['order_items_by_size'].keys():
                order[order_item_id]['order_items_by_size'][size] += quantity
            else:      
                order[order_item_id]['order_items_by_size'][size] = quantity
        else:
            order[order_item_id] = {'order_items_by_size': {size: quantity}}
    else:        
        if order_item_id in list(order.keys()):
             order[order_item_id] += quantity
        
        else:
            order[order_item_id] = quantity

    request.session['order'] = order
    return redirect(redirect_url)
    