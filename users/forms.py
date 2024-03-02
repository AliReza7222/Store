from django import forms
from .models import Profile
import re


class UserProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'phone',
            'about',
            'address',
            'gender'
        )
        help_texts = {
            'phone': 'The phone number must be Iranian and start with 09 .'
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if re.findall('^09[0-9]{9}$', phone):
            return phone
        raise forms.ValidationError('Enter the phone number correctly (start with 09 ).')

