# quiz/urls.py
from django.urls import path
from . import views

app_name = 'quiz'  # Optional but recommended for namespacing

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
]
