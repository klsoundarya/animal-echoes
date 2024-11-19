# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from cloudinary.models import CloudinaryField

# Create your models here.

# class Profile(models.Model):
#     TITLE_CHOICES = [
#         ('Child', 'Child'),
#         ('Parent', 'Parent'),
#         ('Teacher', 'Teacher'),
#         ('Guardian', 'Guardian'),
#         ('Other', 'Other'),
#     ]
    
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(default = 'Steph Burris (Default)', max_length=150, null=True)
#     profile_image = CloudinaryField('image', default='default')
#     title = models.CharField(max_length=200, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#     updated_on = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.username}'s Profile"

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and not instance.is_superuser:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     if not instance.is_superuser:
#         instance.profile.save()
    