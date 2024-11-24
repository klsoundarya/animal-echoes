# echoes/urls.py
from django.urls import path
from .views import EchoList, post_detail, comment_edit, comment_delete, Like_view, submit_blog_post

urlpatterns = [
    path('', EchoList, name='echo_list'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('like/<int:pk>/', Like_view, name='like_post'),
    path('<slug:slug>/edit_comment/<int:comment_id>/', comment_edit, name='comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>/', comment_delete, name='comment_delete'),
    path('submit-blog/', submit_blog_post, name='submit_blog_post'),
]
