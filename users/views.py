from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import User, Profile
from .forms import UserProfile


class CreateProfile(LoginRequiredMixin, CreateView):
    model = Profile
    login_url = 'account_login'
    form_class = UserProfile
    template_name = 'profile.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            Profile.objects.create(user_id=request.user.id, **form.cleaned_data)
            messages.success(request, 'Your profile has been created successfully . ')
            return redirect('users:profile')
        return render(request, self.template_name, context={'form': form})


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    login_url = 'account_login'
    form_class = UserProfile
    template_name = 'profile.html'
    extra_context = {'update': True}
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Your profile has been updated successfully . ')
        return super().form_valid(form)
