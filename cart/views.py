from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404

from django.contrib import messages

from items.models import Item

# Create your views here.

def view_cart(request):
    """ A view that renders the cart contents page """

    return render(request, 'cart/cart.html')

def add_to_cart(request, cart_item_id):
    """ Add a quantity of the specified item to the shopping cart """

    item = get_object_or_404(Item, pk=cart_item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'item_size' in request.POST:  
        size = request.POST['item_size']
        print('size',request.POST['item_size'])
    cart = request.session.get('cart', {})

    if size:
        if cart_item_id in list(cart.keys()):
            if size in cart[cart_item_id]['cart_items_by_size'].keys():
                cart[cart_item_id]['cart_items_by_size'][size] += quantity
                messages.success(request, 
                                    (f'Updated size {size.upper()} '
                                     f'{item.name} quantity to '
                                     f'{cart[cart_item_id]["cart_items_by_size"][size]}'))
            else:
                cart[cart_item_id]['cart_items_by_size'][size] = quantity
                messages.success(request,
                                 (f'Added size {size.upper()} '
                                  f'{item.name} to your cart'))
        else:
            cart[cart_item_id] = {'cart_items_by_size': {size: quantity}}
            messages.success(request,
                             (f'Added size {size.upper()} '
                              f'{item.name} to your cart'))
    else:
        if cart_item_id in list(cart.keys()):
            cart[cart_item_id] += quantity
            messages.success(request,
                             (f'Updated {item.name} '
                              f'quantity to {cart[cart_item_id]}'))
        else:
            cart[cart_item_id] = quantity
            messages.success(request, f'Added {item.name} to your cart')

    request.session['cart'] = cart
    #print(request.session['cart'])
    return redirect(redirect_url)
    
def update_cart(request, cart_item_id):
    """ Update quantity of the specified item to the shopping cart """

    item = get_object_or_404(Item, pk=cart_item_id)
    quantity = int(request.POST.get('quantity'))
    size = None   
    if 'item_size' in request.POST:  
        size = request.POST['item_size']
        print('size',request.POST['item_size'])
    cart = request.session.get('cart', {})

    if size:
        if quantity > 0:
            cart[cart_item_id]['cart_items_by_size'][size] = quantity
            messages.success(request,
                             (f'Updated size {size.upper()} '
                              f'{item.name} quantity to '
                              f'{cart[cart_item_id]["cart_items_by_size"][size]}'))

        else:
            del cart[cart_item_id]['cart_items_by_size'][size]
            if not cart[cart_item_id]['cart_items_by_size']:
                cart.pop(cart_item_id)
            messages.success(request,
                             (f'Removed size {size.upper()} '
                              f'{item.name} from your cart'))

    else:
        if quantity > 0:
            cart[cart_item_id] = quantity  
            messages.success(request,
                             (f'Updated {item.name} '
                              f'quantity to {cart[cart_item_id]}'))

        else:
            cart.pop(cart_item_id)
            messages.success(request,
                             (f'Removed {item.name} '
                              f'from your cart'))

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))

def remove_from_cart(request, cart_item_id):
    """Remove the item from the shopping cart"""
    #print('request data',request.POST)
    #print('cart_item_id',cart_item_id)

    try:
        item = get_object_or_404(Item, pk=cart_item_id)
        size = None
        if 'item_size' in request.POST:
            size = request.POST['item_size']
        cart = request.session.get('cart', {})
        #print('item_size in request.POST',cart)

        if size:
            #print('size',cart[cart_item_id]['cart_items_by_size'][size])
            del cart[cart_item_id]['cart_items_by_size'][size]
            if not cart[cart_item_id]['cart_items_by_size']:
                cart.pop(cart_item_id)
                messages.success(request, 
                                    (f'Removed size {size.upper()} '
                                     f'{item.name} quantity to '))
        else:
            cart.pop(cart_item_id)
            messages.success(request, f'Removed {item.name} from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)
 
    except Exception as e:
        return HttpResponse(status=500)