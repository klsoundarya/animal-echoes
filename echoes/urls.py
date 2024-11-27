# echoes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.EchoList, name='echo_list'),
    path('post/<slug:slug>/', views.animal_detail, name='animal_detail'),
    path('like/<int:pk>/', views.Like_view, name='like_post'),
    path('<slug:slug>/edit_comment/<int:comment_id>/', views.comment_edit, name='comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('submit-blog/', views.submit_blog_post, name='submit_blog_post'),
    path('slider-facts/', views.slider_facts_view, name='slider_facts'),
]
