from django import template


register = template.Library()


@register.filter(name='len_books')
def len_books(value):
    # request = value
    user = value.user
    list_book = value.session.get(f'{user}_cart', [])
    books_int = len(list_book)
    return books_int


@register.filter(name='count_book')
def count_book(value, request):
    book_id = str(value)
    user = request.user
    list_book_in_cart = request.session[f'{user}_cart']
    return list_book_in_cart.count(book_id)
