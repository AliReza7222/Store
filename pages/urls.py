from django.urls import path
from .views import (
    HomePageView,
    AboutPage,
    PaymentSimulator,
    SendCode,
    ListBoughtReceipt,
    ListSoldReceipt
     )


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),
    path('payment/', PaymentSimulator.as_view(), name='payment_simulator'),
    path('payment/get_code/', SendCode.as_view(), name='get_code'),
    path('bought_receipt/', ListBoughtReceipt.as_view(), name='bought_receipt'),
    path('sell_receipt/', ListSoldReceipt.as_view(), name='sell_receipt')
]
