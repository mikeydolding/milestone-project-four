from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import TransactionForm


def checkout(request):
    order = request.session.get('order', {})
    if not order:
        messages.error(request, "There's nothing in your order at the moment")
        return redirect(reverse('products'))

    transaction_form = TransactionForm()
    template = 'checkout/checkout.html'
    context = {
        'transaction_form': transaction_form,
    }

    return render(request, template, context)