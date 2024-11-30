from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'), # Logout page (uses Django's built-in LogoutView)
    path('userprofile_update/', views.update_profile_view, name='userprofile_update'),
    path('password_update/', views.password_update_view, name='password_update'),
    path('signup/', views.signup_view, name='account_signup'),
    path('accounts/delete/', views.delete_account, name='delete_account'),
]
