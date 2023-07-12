from django import template


register = template.Library()


@register.filter(name='len_books')
def len_books(value):
    # request = value
    user = value.user
    list_book = value.session[f'{user}_cart']
    books_int = len(list_book)
    return books_int
