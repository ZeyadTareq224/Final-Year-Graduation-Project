from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_normal_user = models.BooleanField(default=False)
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to = 'media/users/profiles/images/', null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"