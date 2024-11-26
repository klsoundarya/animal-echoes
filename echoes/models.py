from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.utils.timezone import now
from datetime import timedelta

STATUS = ((0, "Draft"), (1, "Published"))


class BlogPost(models.Model): 
    """
    Stores a single blog post entry related to :model:`auth.User`.
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
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)
    approve = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on", "author"]

    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        """
        Override save to auto-generate a unique slug for the blog post
        and handle local and cloudinary images.
        """
        # Generate a unique slug if it doesn't exist
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        # Prioritize Cloudinary image, clear local image if a Cloudinary image is set
        if self.featured_image:
            self.featured_image_local = None

        super().save(*args, **kwargs)  # Call the parent save method

    def __str__(self):
        return f"{self.title} | written by {self.author}"


class Comment(models.Model):
    """
    Stores a single comment entry related to :model:`auth.User`
    and :model:`blog.BlogPost`.
    """
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    name = models.CharField(max_length=255, default="Default Name")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    approved_on = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def was_approved_recently(self):
        """
        Check if the comment was approved in the last day.
        """
        return self.approved and self.approved_on and self.approved_on >= now() - timedelta(days=1)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"
