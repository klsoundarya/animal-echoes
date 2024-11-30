from django.views import View
from django.shortcuts import render
from echoes.models import BlogPost
"""
    View for rendering the homepage.

    - Retrieves up to 6 featured blog posts with a status of '1' (published) ordered by creation date (newest first).
    - Renders the 'home/home_page.html' template with the retrieved posts.
"""

class HomePageView(View):
    def get(self, request):
         # Fetch up to 6 published blog posts sorted by creation date
        featured_posts = BlogPost.objects.filter(status=1).order_by(
                '-created_at')[:6]
        
        # Render the homepage template with featured posts
        return render(request, 'home/home_page.html', {
            'featured_posts': featured_posts})
