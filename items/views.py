from django.shortcuts import render, redirect, reverse,  get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Item
# Create your views here.


def all_items(request):
    """ A view to show items, including sort and search queries """

    items = Item.objects.all()
    query = None

    if request.GET:
        if 'query' in request.GET:
            query = request.GET['query']
        if not query:
            messages.error(request, "Enter search criteria!")
            return redirect(reverse('items'))

        queries = Q(name__icontains=query) | Q(description__icontains=query)
        items = items.filter(queries)

    context = {
        'items': items,
        'search_term': query,

    }

    return render(request, 'items/items.html', context)


def item_detail(request, item_id):
    """ A view to show individual items """

    item = get_object_or_404(Item, pk=item_id)

    context = {
        'item': item,
    }

    return render(request, 'items/item_detail.html', context)
