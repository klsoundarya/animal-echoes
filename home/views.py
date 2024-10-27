from django.views import View
from django.shortcuts import render
from echoes.models import BlogPost 

class HomePageView(View):
    
    def get(self, request):
        featured_posts = BlogPost.objects.all()[:6] 
        return render(request, 'home/home_page.html', {'featured_posts': featured_posts})