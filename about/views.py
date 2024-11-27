from django.shortcuts import render

# about/views.py

def about_view(request):
    """
    Renders the About page
    """
    return render(request, 'about/about.html')
