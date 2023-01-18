from .models import Cart



def cart_count(request):
    context = {}
    cart_total = 0

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)

        if cart_items:
            for item in cart_items:
                cart_total += item.quantity
            context['cart_total'] = cart_total

    else:
        context['cart_total'] = 0

    return context

