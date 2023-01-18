from django.urls import path
from .views import view_product, product_detail, add_to_cart, checkout, update_cart


app_name = 'product'

urlpatterns = [
    path('', view_product, name='products'),
    path('product_detail/<int:prod_id>/', product_detail, name='product_detail'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('checkout/', checkout, name="checkout"),
    path('update-cart/', update_cart, name='update-cart')
]
