import re

from django import forms


class CustomTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({'class': 'custom-input'})
        super().__init__(*args, **kwargs)

class PaymentForm(forms.Form):
    email = forms.EmailField(
    widget = forms.EmailInput(attrs={'placeholder': 'Please enter your email .', 'class': 'custom-input'})
    )

    phone_number = forms.CharField(max_length=11,
    widget=forms.TextInput(attrs={'placeholder': 'Please enter your number .', 'class': 'custom-input'}))

    unique_code = forms.CharField(max_length=6,
    widget = forms.TextInput(attrs={"placeholder": "Enter the code sent .", 'class': 'custom-input'}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if re.findall('^09[0-9]{9}$', phone_number):
            return phone_number
        raise forms.ValidationError('Enter Right Phone number (* start with 09) ')

    def clean_unique_code(self):
        unique_code = self.cleaned_data.get('unique_code')
        if unique_code.isdigit():
            return unique_code
        raise forms.ValidationError('invalid unique code !')
