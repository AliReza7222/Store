from django.urls import path
from .views import BookListView, BookDetailView, RegisterBook


urlpatterns = [
    path('', BookListView.as_view(), name='books'),
    path('<uuid:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('create/', RegisterBook.as_view(), name='create_book'),
]
