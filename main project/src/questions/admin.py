from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(UpVote)
admin.site.register(DownVote)