from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models

import datetime
from uuid import uuid4

# A model representing a single post.
class Post(models.Model):
  uniqueId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
  content = models.CharField(max_length=280)
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now=True)
  parent = models.ForeignKey("Post", on_delete=models.CASCADE, null=True)

  # Represents the short post age displayed on the home page.
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
      return str(post_age_days) + 'd'
    
  @property
  def like_count(self):
    likes = Like.objects.filter(post=self)
    return likes.count
  
  def liked_by(self):
    return Like.objects.filter(post=self)

# A model representing a like on a specific post referenced as a foreign key.
class Like(models.Model):
  uniqueId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
  liker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)

# A model representing a moderator action.
class Action(models.Model):
  ACTION_TYPES = (
    ('deletion', 'Deletion'),
  )

  ACTION_SCOPE = (
    ('personal', 'Personal'),
    ('moderative', 'Moderative'),
  )

  uniqueId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="user_action_set")
  type = models.CharField(max_length=20, choices=ACTION_TYPES)
  scope = models.CharField(max_length=20, choices=ACTION_SCOPE)
  target = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="target_action_set", null=True)
  post = models.UUIDField()
  action_performed_at = models.DateTimeField(auto_now=True)

# A model representing a Mute - a Mute is created whenever a user is muted.
class Mute(models.Model):
  uniqueId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
  target = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="moderator_mute_set")
  reason = models.CharField(max_length=300)