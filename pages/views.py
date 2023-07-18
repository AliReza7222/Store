import string
import random

from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.views.generic import TemplateView, FormView, RedirectView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import BoughtReceipt
from .forms import PaymentForm
from .script import Token
from .mixins import CheckQuantityMixin
from accounts.models import Profile, User
from books.models import Book
from cart.views import get_total_price


def get_error(errors):
    for field in errors:
        return errors.get(field).as_text().lstrip('* ')


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPage(TemplateView):
    template_name = 'pages/about.html'


class PaymentSimulator(LoginRequiredMixin, CheckQuantityMixin, FormView):
    login_url = 'login'
    model = Profile
    form_class = PaymentForm
    template_name = 'pages/payment_simulator.html'

    def get(self, request, *args, **kwargs):
        total_price = get_total_price(request)
        context = self.get_context_data()
        context['total_price'] = total_price
        return self.render_to_response(context)

    def payment_books(self, list_books, user):
        buyer = Profile.objects.get(user=user)
        error_list = []
        for book_id in list_books:
            book = Book.objects.get(id=book_id)
            sell = book.sell_book(buyer)
            if not sell:
                error_list.append(book)
        return error_list

    def create_text_receipt(self, op, dict_books, user, total_price=None):
        obj_code_token = Token()
        receipt = None
        if op == 'buy':
            # error ---->>> receipt one seller with books
            dict_bought = {'seller':[], 'quantity': [], 'title':[], 'price':[]}
            for book, num_book in dict_books.items():
                print(f"{book.price * num_book}", '1111111111')
                dict_bought["seller"].append(book.user.id)
                dict_bought['quantity'].append(f"{book.price} $ x {num_book}")
                dict_bought['title'].append(f"{book.title[:15]}...")
                dict_bought['price'].append(f"{book.price * num_book} $")
            get_code_token = obj_code_token.encoder('buy')
            client = user
            receipt = BoughtReceipt.objects.create(client=client,
                        message=f"{dict_bought}", token=get_code_token, total_price=str(total_price))
        elif op == 'sell':
            ...
        return receipt

    def post(self, request, *args, **kwargs):
        user = request.user
        form = PaymentForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            error = False
            message = None
            if not Profile.objects.filter(user__email = data.get('email'), phone = data.get('phone_number')).exists():
                message = 'phone number or email is not for you'
                error = True

            elif cache.get(str(user.id)) != data.get('unique_code') and cache.get(str(user.id)) != None:
                message = 'invalid unique code !'
                error = True

            elif cache.get(str(user.id)) == None:
                error = True

            elif Profile.objects.get(user__email=data.get('email')).money < get_total_price(request):
                message = f"You do not have { get_total_price(request) } $ in your account"
                error = True

            if error:
                cache.delete(str(user.id))
                if message:
                    messages.error(request, message)
                messages.error(request, f'Your unique code has expired !')
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                # clear cart and calculator sale and buy money
                list_books = request.session[f'{user}_cart']
                error_list = self.payment_books(list_books, user)
                if not error_list:
                    total_price = get_total_price(request)
                    cache.delete(str(user.id))
                    del request.session[f'{user}_cart']
                    message = 'The buy of the books was done successfully'
                    books_dict = {}
                    for book in list_books:
                        books_dict[Book.objects.get(id=book)] = list_books.count(book)
                    receipt_bought = self.create_text_receipt('buy', books_dict, user, total_price=total_price)
                    token_receipt_bought = receipt_bought.token
                    message = f'your shopping has been successfully with tracking code f{token_receipt_bought}.'
                    messages.success(request, message)
                    # sell

                    return redirect('bought_receipt')
                else:
                    cache.delete(str(user.id))
                    for book in error_list:
                        title = book.title
                        message = f"The inventory of {title[:15]}... book has ended"
                        messages.error(request, message)
                    return redirect('my_cart')
        else:
            if cache.get(str(user.id)) != None:
                cache.delete(str(user.id))
                messages.error(request, f'Your unique code has expired !')
            message = get_error(form.errors)
            messages.error(request, message)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])


class SendCode(LoginRequiredMixin, RedirectView):
    login_url = 'login'

    def generate_code(self):
        code = ''.join(random.choices(list(string.digits), k=6))
        return code

    def get(self, request, *args, **kwargs):
        total_price = get_total_price(request)
        code = self.generate_code()
        user = request.user
        message = f'The code is {code} to pay {total_price} dollars to the bookstore of the site '
        subject = 'Pay To BookStore'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [request.user.email]
        send_mail(
        subject,
        message,
        from_email,
        recipient_list
        )
        print(code)
        cache.set(str(user.id), str(code), 78)
        message_success_send = 'The payment code has been sent to your email !'
        return JsonResponse({'message': message_success_send})


class ListBoughtReceipt(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = BoughtReceipt
    paginate_by = 14
    context_object_name = 'receipts_buy'
    template_name = 'pages/receipt_bought.html'

    def get_queryset(self):
        user = self.request.user
        receipts_buy = BoughtReceipt.objects.filter(client=user).order_by('-time_bought')
        queryset = receipts_buy
        if self.extra_context is None:
            self.extra_context = {}
        self.extra_context['seller'] = []
        self.extra_context['title'] = []
        self.extra_context['quantity'] = []
        self.extra_context['price'] = []
        for receipt in receipts_buy:
            message = eval(receipt.message)
            self.extra_context['seller'].append(
                list(map(lambda user_id: User.objects.get(id=user_id), message.get('seller')))
            )
            self.extra_context['quantity'].append(message.get('quantity'))
            self.extra_context['title'].append(message.get('title'))
            self.extra_context['price'].append(message.get('price'))
        return queryset
