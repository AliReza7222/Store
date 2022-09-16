from django.contrib import admin
from .models import Book, Review


class ReviewInline(admin.TabularInline):
    model = Review


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [
        ReviewInline
    ]
    list_display = [
        'title',
        'author',
        'price'
    ]


@admin.register(Review)
class ReviewAdminPanel(admin.ModelAdmin):
    readonly_fields = ['author', 'book']
