import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import User


class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=33)
    author = models.CharField(max_length=200)
    about_book = models.TextField()
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    cover = models.ImageField(upload_to='covers/')

    def delete(self, using=None, keep_parents=False):
        self.cover.storage.delete(str(self.cover.name))
        return super().delete()

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': str(self.pk)})

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    review = models.TextField()
    date = models.DateField(auto_now=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Review_{self.book}'
