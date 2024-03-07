from django.shortcuts import redirect
from django.contrib import messages


class CheckOwnerMixin:

    def invalid_user(self):
        messages.error(self.request, "you don't enter this page .")
        return redirect('books')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            return self.invalid_user()
        return super().dispatch(request, *args, **kwargs)
