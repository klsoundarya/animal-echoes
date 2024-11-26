from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import signup_view, login_view, update_profile_view, password_update_view


app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('userprofile_update/', update_profile_view, name='userprofile_update'),
    path('password_update/', password_update_view, name='password_update'),
    path('signup/', signup_view, name='account_signup'),
]
