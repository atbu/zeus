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
    post_age_secs = int(post_age.total_seconds())
    post_age_mins = int(post_age_secs / 60)
    post_age_hrs = int(post_age_mins / 60)
    post_age_days = int(post_age_hrs / 24)
    
    if(post_age_secs < 60):
      return str(post_age_secs) + 's'
    if(post_age_mins < 60):
      return str(post_age_mins) + 'm'
    if(post_age_hrs < 24):
      return str(post_age_hrs) + 'h'
    else:
      return str(post_age_days) + 'days'

class Like(models.Model):
  uniqueId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
  liker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)

class ModeratorAction(models.Model):
  ACTION_TYPES = (
    ('deletion', 'Deletion'),
  )
  uniqueId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
  moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="moderator_moderatoraction_set")
  type = models.CharField(max_length=20, choices=ACTION_TYPES)
  target = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="target_moderatoraction_set")
  post = models.UUIDField()