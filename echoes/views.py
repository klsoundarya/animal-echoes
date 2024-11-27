from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from .models import BlogPost, Comment, FunFactSlider
from .forms import CommentForm, BlogPostForm


def slider_facts_view(request):
    echo_list = BlogPost.objects.filter(status=1)
    slider_facts = FunFactSlider.objects.all()
    return render(request, 'echoes/slider_facts.html', {
        'echo_list': echo_list,
        'slider_facts': slider_facts,
    })


def EchoList(request):
    if request.user.is_authenticated:
        blog_posts = BlogPost.objects.filter(status=1).order_by("-date")
    else:
        blog_posts = BlogPost.objects.filter(status=1).order_by("-date")[:6]

    paginator = Paginator(blog_posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
 
    context = {
        'echo_list': page_obj,
        'is_authenticated': request.user.is_authenticated,
        'is_paginated': paginator.num_pages > 1, 
    }

    return render(request, 'echoes/echoes.html', context)



def animal_detail(request, slug):
    """
    Display an individual BlogPost with its comments, like status, and the ability to submit new comments.

    **Context**
    - ``post``: The BlogPost instance.
    - ``comments``: All comments for the post, ordered by creation date.
    - ``comment_count``: The count of approved comments.
    - ``comment_form``: The form for submitting a new comment.
    - ``liked``: Whether the current user has liked the post.
    - ``total_likes``: The total number of likes for the post.

    **Template:** echoes/animal_detail.html"""
     
    queryset = BlogPost.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)


    # Like and comment logic
    liked = (
        post.id in request.session.get('liked_posts', [])
        if not request.user.is_authenticated
        else post.likes.filter(id=request.user.id).exists()
    )

    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            messages.success(request, 'Comment submitted and awaiting approval.')
            return redirect('animal_detail', slug=slug) 

    else:
        comment_form = CommentForm()

    return render(
        request,
        "echoes/animal_detail.html",
        {"post": post,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
        "liked": liked,
        "total_likes": post.total_likes(),
        },
    )


def Like_view(request, pk):
    """
    Handles the like/unlike functionality for a post.
    """
    post = get_object_or_404(BlogPost, id=pk)

    if not request.user.is_authenticated:
        liked_posts = request.session.get('liked_posts', [])
        
        if pk in liked_posts:
            liked_posts.remove(pk)  # Unlike
        else:
            liked_posts.append(pk)  # Like

        request.session['liked_posts'] = liked_posts
        request.session.modified = True

    else:
        # Authenticated user: Toggle the like
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    return HttpResponseRedirect(reverse('animal_detail', args=[post.slug]))


@login_required
def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = BlogPost.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.approved_on = None
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment updated successfully!')
        else:
            messages.add_message(request, messages.ERROR, 'Failed to update the comment. Please correct the errors.')

    return HttpResponseRedirect(reverse('animal_detail', args=[slug]))

@login_required
def comment_delete(request, slug, comment_id):
    """
    Delete an individual comment.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.
    ``comment``
        A single comment related to the post.
    """
    queryset = BlogPost.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('animal_detail', args=[slug]))


def submit_blog_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.status = 0 
            blog_post.save()
            messages.success(request, "Your blog post is under review!<br> Approval may take up to two days. Stay tuned!")

            return redirect('home') 
    else:
        form = BlogPostForm()
    
    return render(request, 'echoes/submit_blog_post.html', {'form': form})
