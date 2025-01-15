from django.conf import settings
from django.db import models

from uuid import uuid4

# Create your models here.
class Post(models.Model):
  uniqueId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
  content = models.CharField(max_length=280)
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
  uniqueId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
  liker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)