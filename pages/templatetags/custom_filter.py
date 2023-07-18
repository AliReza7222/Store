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


@register.filter(name='time_strftime')
def time_strftime(value):
    return value.strftime('%Y-%m-%d %H:%M:%S')


@register.filter(name="real_type")
def real_type(value):
    return eval(value)


@register.filter(name='return_index')
def return_index(value, index):
    print(value, index-1)
    return value[index-1]
