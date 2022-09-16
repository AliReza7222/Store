from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import User, Profile
from .forms import UserProfile


class CreateProfile(LoginRequiredMixin, CreateView):
    model = Profile
    template_name = 'profile.html'
    form_class = UserProfile
    login_url = '/accounts/login/'
    redirect_field_name = 'home'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = request.user
        profile_exists = Profile.objects.filter(user_id=user.id).exists()
        if form.is_valid():
            Profile.objects.update_or_create(user_id=user.id, defaults=form.cleaned_data)
            message = ''
            if not profile_exists:
                message = 'Your profile has been created successfully . '
            elif profile_exists:
                message = 'Your profile has been edited successfully . '
            messages.success(request, message)
            return redirect('profile')
        return render(request, self.template_name, context={'form': form})


class UpdateProfile(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Profile
    fields = '__all__'
    template_name = 'profile.html'
    extra_context = {'update': True}
    success_url = '/accounts/profile/'
