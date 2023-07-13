from django.urls import path

from .views import CartShopping, RemoveFromCart, IncrementDecrementBook



urlpatterns=[
    path('my_cart/', CartShopping.as_view(), name='my_cart'),
    path('remove_from_cart/<uuid:book_pk>/', RemoveFromCart.as_view(), name='remove_from_cart'),
    path('increment_decrementbook/<str:op>/<uuid:id_book>/', IncrementDecrementBook.as_view(), name='increment_decrementbook')
]
