import uuid

from users.models import User

from django.db import models


class BoughtReceipt(models.Model):
    id = models.UUIDField(
            primary_key = True,
            default = uuid.uuid4,
            editable = False
    )
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.CharField(max_length=15, editable=False)
    message = models.TextField(editable=False)
    time_bought = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=32, editable=False)

    def __str__(self):
        return f"Receipt Bought {self.time_bought.strftime('%Y-%m-%d %H:%M:%S')}"


class SoldReceipt(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client')
    title = models.CharField(max_length=33, editable=False)
    quantity = models.PositiveIntegerField(default=1, editable=False)
    time_sold = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, editable=False)
    token = models.CharField(max_length=32, editable=False)

    def __str__(self):
        return f"Recipient Sold {self.time_sold.strftime('%Y-%m-%d %H:%M:%S')}"
