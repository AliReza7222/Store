from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import User
from .forms import UserProfile


class CreateProfile(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'profile.html'
    form_class = UserProfile
    login_url = '/accounts/login/'
    redirect_field_name = 'home'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = request.user
        form.instance.user = user
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been created successfully . ')
            return redirect('profile')
        return render(request, self.template_name, context={'form': form})

