from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, Review
from .forms import ReviewForm


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
