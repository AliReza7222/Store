from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView, FormView
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterUser, LoginForm


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
        return render(request, 'signup.html', context={'form': form})


class LoginUser(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        data = request.POST
        username, email, password = data.get('username'), data.get('email'), data.get('password')
        user = authenticate(request, username=username, email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, 'login in site .')
            return redirect('home')
        return redirect('login')


