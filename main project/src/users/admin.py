from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from .models import Profile, ApprovedDoctors

admin.site.register(get_user_model())
admin.site.register(Profile)
admin.site.register(ApprovedDoctors)