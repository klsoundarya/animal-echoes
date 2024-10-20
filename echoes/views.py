from django.shortcuts import render
from django.views import generic
from .models import BlogPost

class EchoList(generic.ListView):
    queryset = BlogPost.objects.all()
    template_name = 'echoes/echo_list.html' 
    context_object_name = 'object_list'
