from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView
from django.http import HttpResponseRedirect
from django.contrib import messages

from books.models import Book


class CartShopping(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        user = request.user
        context = dict()
        my_cart = list(map(lambda book_id: Book.objects.get(id=book_id), request.session.get(f'{user}_cart')))
        total_price = 0
        for book in my_cart:
            total_price += book.price
        print(total_price)
        context['my_cart'] = my_cart
        return render(request, 'cart/my_cart.html', context=context)


class RemoveFromCart(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        user = request.user
        book_id = str(Book.objects.get(pk=kwargs.get('book_pk')).id)
        book = Book.objects.get(id=book_id)
        my_cart = request.session.get(f'{user}_cart')
        del my_cart[my_cart.index(book_id)]
        request.session[f'{user}_cart'] = my_cart
        message = f'book {book} remove from your cart .'
        messages.success(request, message)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
