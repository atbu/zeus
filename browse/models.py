from django.conf import settings
from django.db import models

import datetime
from uuid import uuid4

# Create your models here.
class Post(models.Model):
  uniqueId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
  content = models.CharField(max_length=280)
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now=True)

  @property
  def short_age(self):
    post_age = datetime.datetime.now(datetime.timezone.utc) - self.created_at
    post_age_secs = post_age.total_seconds()
    if(post_age_secs < 60):
      return str(int(post_age_secs)) + 's'
    if(post_age_secs / 60 < 60):
      return str(int(post_age_secs / 60)) + 'm'
    if(post_age_secs / 60 / 24 < 24):
      return str(int(post_age_secs / 60 / 24)) + 'h'
    else:
      return str(int(post_age_secs / 60 / 24 / 365)) + 'days'

class Like(models.Model):
  uniqueId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
  liker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)