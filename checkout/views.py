from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import TransactionForm


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('items'))

    transaction_form = TransactionForm()
    template = 'checkout/checkout.html'
    context = {
        'transaction_form': transaction_form,
    }

    return render(request, template, context)