from django.contrib import admin

from .models import BoughtReceipt, SoldReceipt


admin.site.register(BoughtReceipt)
admin.site.register(SoldReceipt)
