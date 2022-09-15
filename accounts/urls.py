from django.urls import path
from .views import CreateProfile, UpdateProfile

urlpatterns = [
    path('profile/', CreateProfile.as_view(), name='profile'),
    path('profile/update/<uuid:pk>/', UpdateProfile.as_view(), name='update-profile')
]
