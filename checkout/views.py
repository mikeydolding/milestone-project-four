from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import ActionForm


def checkout(request):
    order = request.session.get('order', {})
    if not order:
        messages.error(request, "There's nothing in your order at the moment")
        return redirect(reverse('products'))

    action_form = ActionForm()
    template = 'checkout/checkout.html'
    context = {
        'action_form': action_form,
    }

    return render(request, template, context)