from books.models import Book
from django.contrib import messages
from django.http import HttpResponseRedirect

# custom mxin


class CheckQuantityMixin:

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        my_cart = list(map(lambda book_id: Book.objects.get(id=book_id), request.session.get(f"{user}_cart", [])))
        for book in my_cart:
            if book.quantity == 0:
                message = f"The inventory of {book.title[:15]}... book has ended"
                messages.error(request, message)
                return HttpResponseRedirect(request.META["HTTP_REFERER"])
        return super().dispatch(request, *args, **kwargs)
