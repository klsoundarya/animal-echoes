from django.urls import path
from .views import profile_view
from django.contrib.auth.views import LogoutView
from allauth.account.views import LoginView, SignupView

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('login/', LoginView.as_view(), name='account_login'), 
    path('register/', SignupView.as_view(), name='account_signup'), 
]

