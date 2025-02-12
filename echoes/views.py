from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import BlogPost, Comment, GuestUser, FunFactSlider
from .forms import CommentForm, BlogPostForm


def EchoList(request):
    """
    View to display a paginated list of published blog posts. 
    If the user is authenticated, all posts are shown, otherwise, 
    only the first 6 are displayed.

    - Context
    ``echo_list``
        A paginated list of blog posts.
    ``slider_facts``
        A list of fun facts for the slider display.
    ``is_authenticated``
        Boolean indicating whether the user is authenticated.
    ``is_paginated``
        Boolean indicating whether the posts are paginated.
    """
    if request.user.is_authenticated:
        blog_posts = BlogPost.objects.filter(status=1).order_by("-date")
    else:
        blog_posts = BlogPost.objects.filter(status=1).order_by("-date")[:6]

    paginator = Paginator(blog_posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Add slider_facts to the context
    slider_facts = FunFactSlider.objects.all()

    context = {
        'echo_list': page_obj,
        'slider_facts': slider_facts,
        'is_authenticated': request.user.is_authenticated,
        'is_paginated': paginator.num_pages > 1,
    }

    return render(request, 'echoes/echoes.html', context)

def animal_detail(request, slug):
    """
    Display an individual BlogPost with its comments, like status, and the ability to submit new comments.
    """

    post = get_object_or_404(BlogPost, status=1, slug=slug)

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
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
            "liked": liked,
            "total_likes": post.total_likes(),
        },
    )


# like and unlike view
def Like_view(request, pk):
    """
    Handles the like/unlike functionality for a post.
    """
    post = get_object_or_404(BlogPost, id=pk)

    if not request.user.is_authenticated:
        liked_posts = request.session.get('liked_posts', [])
        if pk in liked_posts:
            liked_posts.remove(pk)  # Unlike
            post.unauthenticated_likes = max(0, post.unauthenticated_likes - 1)
        else:
            liked_posts.append(pk)  # Like
            post.unauthenticated_likes += 1

        request.session['liked_posts'] = liked_posts
        request.session.modified = True
        post.save()

    else:

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    return HttpResponseRedirect(reverse('animal_detail', args=[post.slug]))


@login_required
def comment_edit(request, slug, comment_id):
    """
    Allows authenticated users to edit their own comments on a blog post. 
    The comment is set to 'awaiting approval' after being edited.

    - Context
    ``post``
        The blog post associated with the comment.
    ``comment``
        The comment being edited.
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
    Allows authenticated users to delete their own comments on a blog post.

    - Context

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
    """
    Allows authenticated and guest users to submit a new blog post. The post 
    is saved with a 'pending' status and awaits admin approval.

    - Context
    ``form``
        The form for submitting a new blog post.
    """
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)

            if request.user.is_authenticated:
                blog_post.author = request.user
            else:
                guest_user, created = GuestUser.objects.get_or_create(name="Guest")
                blog_post.guest_author = guest_user

            blog_post.status = 0
            blog_post.save()

            messages.success(request, "Your blog post is under review!")
            return redirect('home')
    else:
        form = BlogPostForm()

    return render(request, 'echoes/submit_blog_post.html', {'form': form})
