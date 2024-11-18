from django.urls import path
from .views import signup_view, login_view, profile_view
from django.contrib.auth.views import LogoutView

app_name = 'accounts' 

urlpatterns = [
    path('login/', login_view, name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('profile/', profile_view, name='profile'), 
    path('signup/', signup_view, name='account_signup'),
]