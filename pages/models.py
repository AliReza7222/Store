import uuid

from accounts.models import User

from django.db import models


class BoughtReceipt(models.Model):
    id = models.UUIDField(
            primary_key = True,
            default = uuid.uuid4,
            editable = False
    )
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client')
    total_price = models.CharField(max_length=15, editable=False)
    message = models.TextField(editable=False)
    time_bought = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=32, editable=False)

    def __str__(self):
        return f"Receipt Bought {self.time_bought.strftime('%Y-%m-%d %H:%M:%S')}"
