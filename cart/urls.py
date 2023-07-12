from django.urls import path

from .views import CartShopping, RemoveFromCart



urlpatterns=[
    path('my_cart/', CartShopping.as_view(), name='my_cart'),
    path('remove_from_cart/<uuid:book_pk>/', RemoveFromCart.as_view(), name='remove_from_cart')

]
