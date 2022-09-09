from django.urls import path
from .views import SignUpUser, LoginUser


urlpatterns = [
    path('signup/', SignUpUser.as_view(), name='signup'),
    path('login/', LoginUser.as_view(), name='login'),

]
