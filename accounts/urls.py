from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'accounts' 

urlpatterns = [
    path('login/', views.login_view, name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('profile/', views.profile_view, name='profile'), 
    path('signup/', views.signup_view, name='account_signup'),
]

