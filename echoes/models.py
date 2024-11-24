from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))


class BlogPost(models.Model):
    """
    Stores a single blogpost entry related to :model:`auth.User`.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="animal_blog_posts")
    featured_image = CloudinaryField('image', null=True, blank=True, default=None)
    featured_image_local = models.ImageField(upload_to='animal_images/', null=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    sound_cloudinary = CloudinaryField('sound', resource_type='auto', null=True, blank=True)
    sound_local = models.FileField(upload_to='animal_sounds/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_posts')

    class Meta:
        ordering = ["-created_on", "author"]

    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):

        if self.featured_image:
            self.local_image = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} | written by {self.author}"

class Comment(models.Model):
    """
    Stores a single comment entry related to :model:`auth.User`
    and :model:`blog.Post`.
    """
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    name = models.CharField(max_length=255, default="Default Name")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]
    
    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"