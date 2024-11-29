from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Login page
    path('login/', views.login_view, name='account_login'),
    # Logout page (uses Django's built-in LogoutView)
    path('logout/', LogoutView.as_view(), name='account_logout'),
    # User profile update page
    path('userprofile_update/', views.update_profile_view, name='userprofile_update'),
    # Password update page
    path('password_update/', views.password_update_view, name='password_update'),
    # Signup page
    path('signup/', views.signup_view, name='account_signup'),
]
