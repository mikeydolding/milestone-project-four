from django.shortcuts import render, redirect

# Create your views here.

def view_order(request):
    """ A view that renders the order contents page """

    return render(request, 'order/order.html')

def add_to_order(request, item_id):
    """ Add a quantity of the specified product to the shopping order """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    order = request.session.get('order', {})

    if item_id in list(order.keys()):
        order[item_id] += quantity
    else:
        order[item_id] = quantity

    request.session['order'] = order
    return redirect(redirect_url)
    