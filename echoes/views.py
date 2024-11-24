from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import BlogPost, Comment
from .forms import CommentField


class EchoList(generic.ListView):
    queryset = BlogPost.objects.filter(status=1).order_by("-created_on")
    template_name = 'echoes/echoes.html'
    context_object_name = 'echo_list'
    paginate_by = 6

def post_detail(request, slug):
    """
    Display an individual BlogPost with its comments, like status, and the ability to submit new comments.

    **Context**
    - ``post``: The BlogPost instance.
    - ``comments``: All comments for the post, ordered by creation date.
    - ``comment_count``: The count of approved comments.
    - ``comment_form``: The form for submitting a new comment.
    - ``liked``: Whether the current user has liked the post.
    - ``total_likes``: The total number of likes for the post.

    **Template:** echoes/post_detail.html"""
     
    queryset = BlogPost.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)

    liked = post.likes.filter(id=request.user.id).exists() if request.user.is_authenticated else False

    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    if request.method == "POST":
        comment_form = CommentField(data=request.POST)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            messages.success(request, 'Comment submitted and awaiting approval.')
            return redirect('post_detail', slug=slug) 

    else:
        comment_form = CommentField()

    return render(
        request,
        "echoes/post_detail.html",
        {"post": post,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
        "liked": liked,
        "total_likes": post.total_likes(),
        },
    )


@login_required
def Like_view(request, pk):
    """
    Handles the like/unlike functionality for a post.
    """
    post = get_object_or_404(BlogPost, id=pk)

    if request.user.is_authenticated:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[post.slug]))



# def comment_edit(request, slug, comment_id):
#     """
#     Allow a user to edit their own comment.
#     """
#     post = get_object_or_404(BlogPost, slug=slug, status=1)
#     comment = get_object_or_404(Comment, pk=comment_id, author=request.user)

#     if request.method == "POST":
#         comment_form = CommentField(request.POST, instance=comment)
#         if comment_form.is_valid():
#             comment_form.save()
#             messages.success(request, "Comment updated successfully!")
#         else:
#             messages.error(request, "Failed to update the comment. Please try again.")
#         return redirect("post_detail", slug=slug)

#     # non-POST requests (fallback)
#     messages.error(request, "Invalid request.")
#     return redirect("post_detail", slug=slug)

def comment_edit(request, slug, comment_id):
    post = get_object_or_404(BlogPost, slug=slug, status=1)
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == 'POST':
        form = CommentField(request.POST, instance=comment)
        if form.is_valid():
            form.save() 
            messages.success(request, "Comment updated successfully!")
            return redirect("post_detail", slug=slug) 
        else:
            messages.error(request, "Failed to update the comment. Please correct the errors.")
    else:
        form = CommentField(instance=comment)

    return render(request, 'post_detail.html', {'form': form, 'comment': comment, 'post': post, 'slug': slug})


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
        messages.add_message(request, messages.ERROR,
                             'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))