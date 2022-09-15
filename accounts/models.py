import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    GENDER_CHOICE = (
        ('m', 'Male'),
        ('f', 'Female')
    )
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=1)
    phone = models.CharField(max_length=11)
    about = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
