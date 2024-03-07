from django.urls import path
from .views import CreateProfile, UpdateProfile


app_name = 'users'
urlpatterns = [
    path('profile/', CreateProfile.as_view(), name='profile'),
    path('profile/update/<uuid:pk>/', UpdateProfile.as_view(), name='update_profile')
]
