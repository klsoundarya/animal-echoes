# echoes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('echoes/', views.EchoList.as_view(), name='echo_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),

]
