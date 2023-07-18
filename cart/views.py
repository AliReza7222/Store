from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView, FormView
from django.http import HttpResponseRedirect
from django.contrib import messages

from books.models import Book


def get_total_price(request):
    user = request.user
    my_cart = list(map(lambda book_id: Book.objects.get(id=book_id), request.session.get(f'{user}_cart', [])))
    total_price = 0
    for book in my_cart:
        total_price += book.price
    return total_price


class CartShopping(LoginRequiredMixin, RedirectView):

    def uniq_list(self, value):
        new_list = list()
        for index_value in value:
            if index_value not in new_list:
                new_list.append(index_value)
        return new_list

    def get(self, request, *args, **kwargs):
        user = request.user
        context = dict()
        my_cart = list(map(lambda book_id: Book.objects.get(id=book_id), request.session.get(f'{user}_cart', [])))
        total_price = get_total_price(request)
        context['total_price'] = total_price
        context['my_cart'] = self.uniq_list(my_cart)
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


class IncrementDecrementBook(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        user = request.user
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
