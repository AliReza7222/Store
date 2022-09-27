from django import forms
from .models import Review, Book


class FormRegisterBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'about_book',
            'publication_date',
            'price',
            'quantity',
            'cover'
        ]
        widgets = {
            'publication_date': forms.DateInput(attrs={'placeholder': 'for example: 2010-10-10'}),
        }


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('review', )
        widgets = {
            'review': forms.Textarea(attrs={'placeholder': 'Write your opinion about the book.'})
        }
