from logging import Logger

from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from .models import Book, Review
from .mixins import *
from .forms import ReviewForm, FormRegisterBook


class RegisterBook(LoginRequiredMixin, CreateView):
    model = Book
    login_url = 'account_login'
    template_name = 'books/register_book.html'
    form_class = FormRegisterBook

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            data['user'] = request.user
            Book.objects.create(**data)
            messages.success(request, 'your book has been successfully created .')
            return redirect('books')
        return render(request, self.template_name, context={'form': form})


class BookListView(ListView):
    model = Book
    paginate_by = 20
    template_name = 'books/book_list.html'
    context_object_name = 'book_list'
    ordering = ['-quantity']


class BookDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Book
    login_url = 'account_login'
    form_class = ReviewForm
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        my_cart = request.session.get(f'{request.user}_cart', ['None'])
        if 'None' not in my_cart:
            my_cart = list(map(lambda book_id: Book.objects.get(id=book_id), my_cart))
        context['my_cart'] = my_cart
        context['user_book'] = self.object.user
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            Review.objects.create(
                book=self.object,
                author=request.user,
                review=form.cleaned_data.get('review')
            )
            messages.success(request, 'Your comment has been successfully created.')
            return redirect('book_detail', pk=kwargs.get('pk'))
        messages.error(request, 'Error for create post.')
        return redirect('book_detail', pk=kwargs.get('pk'))


class UpdateBook(LoginRequiredMixin, CheckOwnerMixin, UpdateView):
    model = Book
    login_url = 'account_login'
    form_class = FormRegisterBook
    template_name = 'books/register_book.html'
    extra_context = {'update': True}
    context_object_name = 'books'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(
            request,
            f"Book {self.object.title} updated successfully ."
        )
        self.success_url = "/books/mybooks/"
        return super().post(request, *args, **kwargs)


class DeleteBook(LoginRequiredMixin, CheckOwnerMixin, DeleteView):
    model = Book
    login_url = 'account_login'
    template_name = 'books/delete_object.html'
    context_object_name = 'book'
    success_url = reverse_lazy('mybooks')


class MyBooks(LoginRequiredMixin, ListView):
    login_url = 'account_login'
    paginate_by = 30
    model = Book
    template_name = 'books/my_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        my_books = self.model.objects.filter(user=self.request.user)
        return my_books


class SearchBook(ListView):
    model = Book
    template_name = 'books/search_books.html'
    context_object_name = 'books_list'

    def get_queryset(self):
        query_key = self.request.GET.get('search_input')
        return self.model.objects.filter(
            Q(title__icontains=query_key)
        )


class FavouriteBook(LoginRequiredMixin, FormView):
    login_url = 'account_login'
    model = Book
    template_name = 'books/book_detail.html'

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs.get('pk'))
        if book.favourites.filter(pk=request.user.pk).exists():
            messages.success(request, 'this book remove of your favourite books .')
            book.favourites.remove(request.user)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            messages.success(request, 'this book add to your favourite books .')
            book.favourites.add(request.user)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class MyFavouriteBooks(LoginRequiredMixin, ListView):
    login_url = 'account_login'
    model = Book
    template_name = 'books/my_fav.html'
    context_object_name = 'books'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        fav_books = Book.objects.filter(favourites=user)
        return fav_books


class AddToCart(LoginRequiredMixin, RedirectView):
    login_url = 'account_login'

    def get(self, request, *args, **kwargs):
        book = Book.objects.get(pk=kwargs.get('book_pk'))
        my_cart = request.session.get(f'{request.user}_cart', [])
        my_cart.append(str(book.id))
        request.session[f'{request.user}_cart'] = my_cart
        message = f'book {book} add to your cart .'
        messages.success(request, message)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
