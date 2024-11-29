from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.utils.timezone import now
from datetime import timedelta, date


STATUS = ((0, "Draft"), (1, "Published"))


class GuestUser(models.Model):
    name = models.CharField(max_length=100, default="Guest")
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """
    Stores a single blog post related to :model:`auth.User` :model:`GuestUser`.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    species = models.CharField(max_length=85, null=True, blank=True)
    habitat = models.CharField(max_length=255, null=True, blank=True)
    diet = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="animal_blog_posts", blank=True, null=True)
    guest_author = models.ForeignKey(GuestUser, on_delete=models.SET_NULL, null=True, blank=True)  # For guest users
    featured_image = CloudinaryField('image', null=True, blank=True, default=None)
    featured_image_local = models.ImageField(upload_to='animal_images/', null=True, blank=True)
    intro = models.TextField(blank=True)
    description = models.TextField()
    sound_cloudinary = CloudinaryField('sound', resource_type='auto', null=True, blank=True)
    sound_local = models.FileField(upload_to='animal_sounds/', null=True, blank=True)
    date = models.DateField("Post Date", default=date.today)
    updated_on = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)
    tags = models.ManyToManyField('Tag', related_name="blog_posts", blank=True)
    fun_facts = models.ManyToManyField('AnimalFact', related_name="blog_posts_facts", blank=True, verbose_name="Fun Facts")
    approve = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS, default=0)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["date", "author"]

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

        # Assign a guest user if no authenticated user is available
        if not self.author:
            # You can create a default guest user if needed
            guest_user, created = GuestUser.objects.get_or_create(name="Guest")
            self.guest_author = guest_user  # Use guest_author for unauthenticated users

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} | written by {self.author if self.author else self.guest_author}"


class BlogPostImage(models.Model):

    blog_post = models.ForeignKey(BlogPost, related_name="image_gallery", on_delete=models.CASCADE)
    image_gallery = CloudinaryField('image', null=True, blank=True, default=None)
    image_gallery_local = models.ImageField(upload_to='animal_gallery_images/', null=True, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"Image {self.position} for {self.blog_post.title}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class AnimalFact(models.Model):
    """
    Stores fun facts about animals.
    """
    animal = models.ForeignKey(BlogPost, related_name='facts', on_delete=models.CASCADE)
    fact_text = models.TextField()

    def __str__(self):
        return f"Fact about {self.animal.title}"


class FunFactSlider(models.Model):
    """
    Stores fun facts and an associated image for the slider.
    """
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, default=1)
    fact_text = models.TextField()
    slider_image = CloudinaryField('image', null=True, blank=True, default=None)
    slider_image_local = models.ImageField(upload_to='slider_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Slider Fact for {self.blog_post}"


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
