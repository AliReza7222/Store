from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
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
            return redirect(f'/books/{kwargs.get("pk")}/')
        messages.error(request, 'Error for create post.')
        return redirect(f'/books/{kwargs.get("pk")}/')


class UpdateBook(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Book
    form_class = FormRegisterBook
    template_name = 'books/register_book.html'
    extra_context = {'update': True}
    context_object_name = 'books'
