from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .models import Book, Review
from .forms import ReviewForm, FormRegisterBook


class RegisterBook(LoginRequiredMixin, CreateView):
    model = Book
    login_url = '/accounts/login/'
    template_name = 'books/register_book.html'
    form_class = FormRegisterBook

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user, cover = request.user, request.FILES.get('cover')
            data = form.cleaned_data
            data['user'] = user
            Book.objects.create(**data)
            messages.success(request, 'your book has been successfully created .')
            return redirect('books')
        return render(request, self.template_name, context={'form': form})


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'book_list'


class BookDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Book
    login_url = '/accounts/login/'
    form_class = ReviewForm
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(id=kwargs.get('pk'))
        author = request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            review = form.cleaned_data.get('review')
            Review.objects.create(
                book=book,
                author=author,
                review=review
            )
            messages.success(request, 'Your comment has been successfully created.')
            return redirect('book_detail', pk=kwargs.get('pk'))
        messages.error(request, 'Error for create post.')
        return redirect('book_detail', pk=kwargs.get('pk'))


class UpdateBook(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Book
    form_class = FormRegisterBook
    template_name = 'books/register_book.html'
    extra_context = {'update': True}
    context_object_name = 'books'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        obj_book = Book.objects.get(pk=kwargs.get('pk'))
        if user != obj_book.user:
            messages.error(request, "you don't enter this page .")
            return redirect('books')
        return super().get(request, *args, **kwargs)


class DeleteBook(LoginRequiredMixin, DeleteView):
    model = Book
    login_url = '/accounts/login/'
    template_name = 'books/delete_object.html'
    context_object_name = 'book'
    success_url = '/books/'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        obj_book = Book.objects.get(pk=kwargs.get('pk'))
        if user != obj_book.user:
            messages.error(request, "you don't enter this page .")
            return redirect('books')
        return super().get(request, *args, **kwargs)


class MyBooks(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Book
    template_name = 'books/my_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        user = self.request.user
        my_books = self.model.objects.filter(user=user)
        return my_books


class SearchBook(ListView):
    model = Book
    template_name = 'books/search_books.html'
    context_object_name = 'books_list'

    def get_queryset(self):
        query_key = self.request.GET.get('search_input')
        return Book.objects.filter(
            Q(title__icontains=query_key) | Q(author__icontains=query_key)
        )


class FavouriteBook(LoginRequiredMixin, FormView):
    login_url = 'login'
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
    login_url = 'login'
    model = Book
    template_name = 'books/my_fav.html'
    context_object_name = 'books'

    def get_queryset(self):
        user = self.request.user
        fav_books = Book.objects.filter(favourites=user)
        return fav_books
