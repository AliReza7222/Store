from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView, FormView
from django.http import HttpResponseRedirect
from django.contrib import messages

from books.models import Book
from .utils import *


class CartShopping(LoginRequiredMixin, RedirectView):
    login_url = 'account_login'

    def get(self, request, *args, **kwargs):
        context = dict()
        my_cart = list(
            map(
                lambda book_id: Book.objects.get(id=book_id),
                request.session.get(f'{request.user}_cart', [])
            )
        )
        context['total_price'] = get_total_price(request)
        context['my_cart'] = self.uniqe_list(my_cart)
        return render(request, 'cart/my_cart.html', context=context)

    def uniqe_list(self, value):
        new_list = list()
        for index_value in value:
            if index_value not in new_list:
                new_list.append(index_value)
        return new_list



class RemoveFromCart(LoginRequiredMixin, RedirectView):
    login_url = 'account_login'

    def get(self, request, *args, **kwargs):
        book = Book.objects.get(id=kwargs.get('book_pk'))
        self.remove_book_from_cart(book)
        messages.success(request, f'book {book} remove from your cart .')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def remove_book_from_cart(self, book):
        cart = self.request.session.get(f'{self.request.user}_cart')
        for book_id in cart.copy():
            if book_id == str(book.id):
                del cart[cart.index(book_id)]
        self.request.session[f'{self.request.user}_cart'] = cart


class IncrementDecrementBook(LoginRequiredMixin, RedirectView):
    login_url = 'account_login'

    def get(self, request, *args, **kwargs):
        op, id_book = kwargs.get('op'), str(kwargs.get('id_book'))
        book = Book.objects.get(id=id_book)
        my_cart = request.session[f'{request.user}_cart']
        book_select = my_cart.count(id_book)
        book_inventory = book.quantity
        if op == 'up' and (book_select + 1) <= book_inventory:
            my_cart.append(id_book)
        elif op == 'down' and (book_select - 1) >= 1:
            del my_cart[my_cart.index(id_book)]
        request.session[f'{request.user}_cart'] = my_cart

        return redirect('my_cart')
