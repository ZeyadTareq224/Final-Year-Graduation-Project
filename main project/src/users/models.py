from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

# Create your models here.

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_normal_user = models.BooleanField(default=False)
    

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
]

BLOOD_GROUPS = [
    ('O-', 'O-'),
    ('O+', 'O+'),
    ('A-', 'A-'),
    ('A+', 'A+'),
    ('B-', 'B-'),
    ('B+', 'B+'),
    ('AB-', 'AB-'),
    ('AB+', 'AB+'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to = 'media/users/profiles/images/', null=True, default="default_user_img.png")
    #phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(max_length=17, blank=True, null=True) # validators should be a list
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f"{self.user.username}'s Profile"