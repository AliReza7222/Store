from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import CreateView
from .forms import RegisterUser


class SignUpUser(CreateView):
    template_name = 'signup.html'
    form_class = RegisterUser

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = self.form_class(data)
        if form.is_valid():
            form.save()
            messages.success(request, message=f"you with username {data.get('username')} register in site .")
            return redirect('home')
        return redirect('signup')
