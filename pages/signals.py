import re

from .models import BoughtReceipt
from django.db.models.signals import post_save
from django.contrib import messages
from django.dispatch import receiver

from .models import SoldReceipt
from decimal import Decimal
from .script import Token
from books.models import Book
from users.models import User


# create receipt sell for own book .

@receiver(post_save, sender=BoughtReceipt)
def sold_receipt(sender, instance, created, **kwargs):
    info = eval(instance.message)
    num_seller = len(info['seller'])
    obj_token = Token()
    for index_list in range(num_seller):
        client = instance.client
        seller = User.objects.get(id=info['seller'][index_list])
        title = info['title'][index_list]
        token = obj_token.encoder('sell')
        quantity = int(re.findall(' [0-9]+', info['quantity'][index_list])[0].lstrip())
        price = Decimal(re.findall('[0-9.]+', info['price'][index_list])[0])
        dict_info = {'price': price, 'client': client, 'seller': seller,
                'title': title, 'token': token, 'quantity': quantity}
        SoldReceipt.objects.create(**dict_info)
