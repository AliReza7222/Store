import re

from django.contrib.auth import get_user_model
from django import forms


class RegisterUser(forms.ModelForm):

    password1 = forms.CharField(max_length=15, min_length=7, widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(max_length=15, min_length=7, widget=forms.PasswordInput(), label='Repeat Password')

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
            "phone_number"
        )

    def clean_password2(self):
        data = self.cleaned_data
        password1, password2 = data.get('password1'), data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords are not the same .")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            if username != re.findall("\w+", username)[0]:
                raise forms.ValidationError("Username must contain numbers and letters.")
            if len(username) < 4:
                raise forms.ValidationError("Username length should be greater than 4 .")
            return username
        except :
            raise forms.ValidationError("Username must contain numbers and letters.")

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        if len(re.findall("^09[0-9]+$", phone_number)) == 1:
            return phone_number
        raise forms.ValidationError("The phone number must be Iranian and start with 0.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
