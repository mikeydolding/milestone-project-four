from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404

from django.contrib import messages

from items.models import Item

# Create your views here.

def view_order(request):
    """ A view that renders the order contents page """

    return render(request, 'order/order.html')

def add_to_order(request, orderItem_id):
    """ Add a quantity of the specified item to the shopping order """

    item = get_object_or_404(Item, pk=orderItem_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'item_size' in request.POST:  
        size = request.POST['item_size']
        print('size',request.POST['item_size'])
    order = request.session.get('order', {})

    if size:
        if orderItem_id in list(order.keys()):
            if size in order[orderItem_id]['orderItems_by_size'].keys():
                order[orderItem_id]['orderItems_by_size'][size] += quantity
            else:
                order[orderItem_id]['orderItems_by_size'][size] = quantity
        else:
            order[orderItem_id] = {'orderItems_by_size': {size: quantity}}
    else:
        if orderItem_id in list(order.keys()):
            order[orderItem_id] += quantity
        else:
            order[orderItem_id] = quantity
            messages.success(request, f'Added {item.name} to your order')

    request.session['order'] = order
    #print(request.session['order'])
    return redirect(redirect_url)
    
def update_order(request, orderItem_id):
    """ Update quantity of the specified item to the shopping order """
    quantity = int(request.POST.get('quantity'))


    size = None   
    if 'item_size' in request.POST:  
        size = request.POST['item_size']
        print('size',request.POST['item_size'])
    order = request.session.get('order', {})

    if size:
        if quantity > 0:
            order[orderItem_id]['orderItems_by_size'][size] = quantity
        else:
            del order[orderItem_id]['orderItems_by_size'][size]
            if not order[orderItem_id]['orderItems_by_size']:
                order.pop(orderItem_id)
    else:
        if quantity > 0:
            order[orderItem_id] = quantity  
        else:
            order.pop(orderItem_id)


    request.session['order'] = order
    return redirect(reverse('view_order'))

def remove_from_order(request, orderItem_id):
    """Remove the item from the shopping order"""
    print('request data',request.POST)
    print('orderItem_id',orderItem_id)

    try:
        size = None
        if 'item_size' in request.POST:
            size = request.POST['item_size']
        order = request.session.get('order', {})
        print('item_size in request.POST',order)

        if size:
            print('size',order[orderItem_id]['orderItems_by_size'][size])

            del order[orderItem_id]['orderItems_by_size'][size]
            if not order[orderItem_id]['orderItems_by_size']:
                order.pop(orderItem_id)



        else:
            order.pop(orderItem_id)

        request.session['order'] = order
        return HttpResponse(status=200)
 
    except Exception as e:
        return HttpResponse(status=500)