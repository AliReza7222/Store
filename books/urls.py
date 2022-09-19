from django.urls import path
from .views import (
        BookListView,
        BookDetailView,
        RegisterBook,
        UpdateBook,
        DeleteBook
    )

urlpatterns = [
    path('', BookListView.as_view(), name='books'),
    path('<uuid:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('create/', RegisterBook.as_view(), name='create_book'),
    path('update/<uuid:pk>/', UpdateBook.as_view(), name='update_book'),
    path('delete/<uuid:pk>/', DeleteBook.as_view(), name='delete_book'),
]
