from django.db import models
from django.contrib.auth import get_user_model

class Article(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=150)
    #tags = models.ForeignKey(Tags)
    #cover_img = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    #comments = models.ForeignKey(Comments, max_length=100)
    up_votes = models.IntegerField()
    down_votes = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
    	return self.title

    def get_votes(self):
        return self.up_votes - self.down_votes