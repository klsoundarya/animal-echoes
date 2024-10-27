from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import BlogPost

class EchoList(generic.ListView):
    queryset = BlogPost.objects.filter(status=1).order_by("-created_on")
    template_name = 'echoes/echoes.html'
    context_object_name = 'echo_list'
    paginate_by = 6

def post_detail(request, slug):
    """
    Display an individual :model:`echoes.BlogPost`.

    **Context**

    ``post``
        An instance of :model:`echoes.BlogPost`.

    **Template:**

    :template:`echoes/post_detail.html`
    """

    queryset = BlogPost.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    return render(
        request,
        "echoes/post_detail.html",
        {"post": post,
        "comments": comments,
        "comment_count": comment_count,
        },
    )