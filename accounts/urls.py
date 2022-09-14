from django.urls import path
from .views import CreateProfile

urlpatterns = [
    path('profile/', CreateProfile.as_view(), name='profile'),
]