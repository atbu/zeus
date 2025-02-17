from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import NewPostForm
from .models import Post, Action, Mute, Like

# Create your views here.
def index(request):
  posts = Post.objects.filter(parent=None).order_by("-created_at")

  logged_in_as = ""
  if(request.user.is_authenticated):
    logged_in_as = request.user.username

  is_user_moderator = request.user.groups.filter(name="Moderators").exists()

  if(logged_in_as == ""):
    liked_post_ids = []
  else:
    user_likes = Like.objects.filter(liker=request.user)
    liked_post_ids = []
    for like in user_likes:
      liked_post_ids.append(like.post.uniqueId)

  context = {
    'posts': posts,
    'logged_in_as': logged_in_as,
    'is_user_moderator': is_user_moderator,
    'liked_post_ids': liked_post_ids,
  }

  return render(request, 'browse/index.html', context)

@login_required
def post_detail(request, post_id):
  post = get_object_or_404(Post, pk=post_id)

  logged_in_as = ""
  if(request.user.is_authenticated):
    logged_in_as = request.user.username

  is_user_moderator = request.user.groups.filter(name="Moderators").exists()

  has_user_liked_this = Like.objects.filter(liker=request.user, post=Post.objects.filter(pk=post_id).first()).exists()

  likes = Like.objects.filter(post=Post.objects.get(uniqueId=post_id))

  context = {
    "post": post,
    "logged_in_as": logged_in_as,
    "is_user_moderator": is_user_moderator,
    "has_user_liked_this": has_user_liked_this,
    "likes": likes,
  }

  return render(request, "browse/post_detail.html", context)

@login_required
def user_detail(request, username):
  user = get_object_or_404(get_user_model(), username=username)
  posts = Post.objects.filter(author__username=username)

  logged_in_as = ""
  if(request.user.is_authenticated):
    logged_in_as = request.user.username

  is_user_moderator = request.user.groups.filter(name="Moderators").exists()

  context = {
    "user": user,
    "posts": posts,
    "logged_in_as": logged_in_as,
    "is_user_moderator": is_user_moderator,
  }

  return render(request, "browse/user_detail.html", context)

@login_required
def new_post(request):
  if(Mute.objects.filter(target=request.user).exists()):
    return HttpResponseRedirect('/browse/muted')
  
  logged_in_as = request.user.username
  is_user_moderator = request.user.groups.filter(name="Moderators").exists()
  
  if request.method == "POST":
    form = NewPostForm(request.POST)
    if(form.is_valid()):
      new_post = form.save(commit=False)
      new_post.author = request.user
      new_post.save()
      return HttpResponseRedirect('/')
  else:
    form = NewPostForm()

  return render(request, "new_post.html", {"form": form, "logged_in_as": logged_in_as, "is_user_moderator": is_user_moderator,})

@login_required
def account_settings(request):
  logged_in_as = request.user.username
  is_user_moderator = request.user.groups.filter(name="Moderators").exists()
  
  return render(request, "account_settings.html", {"logged_in_as": logged_in_as, "is_user_moderator": is_user_moderator,})

@login_required
def delete_post(request, post_id):
  post = Post.objects.get(pk=post_id)

  # Check if they are a moderator.
  if(request.user.groups.filter(name="Moderators").exists()):
    a = Action(user=request.user, type='deletion', scope='moderative', target=post.author, post=post_id)
    a.save()
    Post.objects.filter(pk=post_id).delete()
    return HttpResponseRedirect('/')
  elif(request.user == post.author):
    a = Action(user=request.user, type='deletion', scope='personal', post=post_id)
    a.save()
    Post.objects.filter(pk=post_id).delete()
    return HttpResponseRedirect('/')

@login_required
def toggle_like_post(request, post_id, sender):
  post = Post.objects.get(pk=post_id)
  liker = request.user

  if(Like.objects.filter(post=post, liker=liker).exists()):
    Like.objects.get(post=post, liker=liker).delete()
  else:
    new_like = Like.objects.create(liker=liker, post=post)
    new_like.save()

  if(sender == 'post_detail'):
    return HttpResponseRedirect(reverse('post_detail', args=[post.uniqueId]))
  else:
    return HttpResponseRedirect(reverse('index'))

@login_required
def post_reply(request, post_id, content):
  post = Post.objects.get(pk=post_id)
  replier = request.user

  reply = Post.objects.create(content=content, author=replier, parent=post)
  reply.save()

  return post_detail(request, post_id)

@login_required
def delete_own_user(request):
  user = request.user
  user.is_active = False
  user.save()
  Post.objects.filter(author=user).delete()
  Like.objects.filter(liker=user).delete()
  Mute.objects.filter(target=user).delete()
  return HttpResponseRedirect(reverse('logout'))

def muted(request):
  return render(request, "muted.html", { 'logged_in_as': request.user.username })