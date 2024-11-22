# echoes/urls.py
from django.urls import path
from .views import EchoList, post_detail, comment_edit, comment_delete

urlpatterns = [
    path('', EchoList.as_view(), name='echo_list'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('<slug:slug>/edit_comment/<int:comment_id>',
         comment_edit, name='comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>',
         comment_delete, name='comment_delete'),
]
