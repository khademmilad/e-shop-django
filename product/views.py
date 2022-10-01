from django.shortcuts import render
from .models import Product


def view_products(request):
    context = {}
    products = Product.objects.all()

    if products:
        context['products'] = products

    return render(request, 'product/products.html', context)
