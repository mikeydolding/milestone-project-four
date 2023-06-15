from django.shortcuts import render, redirect

# Create your views here.

def view_order(request):
    """ A view that renders the order contents page """

    return render(request, 'order/order.html')

def add_to_order(request, orderItem_id):
    """ Add a quantity of the specified product to the shopping order """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'orderItem_size' in request.POST:
        size = request.POST['orderItem_size']
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

    request.session['order'] = order
    return redirect(redirect_url)
    