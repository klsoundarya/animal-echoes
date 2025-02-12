from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   
class DeletedUser(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} (deleted at {self.deleted_at})"
