# echoes/urls.py
from django.urls import path
from .views import EchoList, post_detail

urlpatterns = [
    path('', EchoList.as_view(), name='echo_list'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),

]
