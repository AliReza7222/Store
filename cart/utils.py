from books.models import Book


def get_total_price(request):
    user = request.user
    my_cart = list(
        map(
            lambda book_id: Book.objects.get(id=book_id),
            request.session.get(f'{user}_cart', [])
        )
    )
    total_price = 0
    for book in my_cart:
        total_price += book.price
    return total_price
