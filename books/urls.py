from django.urls import path
from .views import *


urlpatterns = [
    path('', BookListView.as_view(), name='books'),
    path('<uuid:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('create/', RegisterBook.as_view(), name='create_book'),
    path('update/<uuid:pk>/', UpdateBook.as_view(), name='update_book'),
    path('delete/<uuid:pk>/', DeleteBook.as_view(), name='delete_book'),
    path('mybooks/', MyBooks.as_view(), name='mybooks'),
    path('results/', SearchBook.as_view(), name='search_results'),
    path('fav/<uuid:pk>/', FavouriteBook.as_view(), name='favourite_book'),
    path('my_fav/', MyFavouriteBooks.as_view(), name='my_fav'),
    path('add_cart/<uuid:book_pk>/', AddToCart.as_view(), name='add_cart'),
]
