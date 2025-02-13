from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .forms import NewPostForm
from .models import Post, Action, Mute, Like

# Create your views here.
def index(request):
  posts = Post.objects.order_by("-created_at")

  logged_in_as = ""
  if(request.user.is_authenticated):
    logged_in_as = request.user.username

  is_user_moderator = request.user.groups.filter(name="Moderators").exists()

  context = {
    'posts': posts,
    'logged_in_as': logged_in_as,
    'is_user_moderator': is_user_moderator,
  }

  return render(request, 'browse/index.html', context)

def post_detail(request, post_id):
  post = get_object_or_404(Post, pk=post_id)

  logged_in_as = ""
  if(request.user.is_authenticated):
    logged_in_as = request.user.username

  is_user_moderator = request.user.groups.filter(name="Moderators").exists()

  has_user_liked_this = Like.objects.filter(liker=request.user, post=Post.objects.filter(pk=post_id).first()).exists()

  context = {
    "post": post,
    "logged_in_as": logged_in_as,
    "is_user_moderator": is_user_moderator,
    "has_user_liked_this": has_user_liked_this,
  }

  return render(request, "browse/post_detail.html", context)

def user_detail(request, username):
  user = get_object_or_404(get_user_model(), username=username)
  posts = Post.objects.filter(author__username=username)

  logged_in_as = ""
  if(request.user.is_authenticated):
    logged_in_as = request.user.username

  context = {
    "user": user,
    "posts": posts,
    "logged_in_as": logged_in_as,
  }

  return render(request, "browse/user_detail.html", context)

@login_required
def new_post(request):
  if(Mute.objects.filter(target=request.user).exists()):
    return HttpResponseRedirect('/browse/muted')
  
  if request.method == "POST":
    form = NewPostForm(request.POST)
    if(form.is_valid()):
      new_post = form.save(commit=False)
      new_post.author = request.user
      new_post.save()
      return HttpResponseRedirect('/')
  else:
    form = NewPostForm()

  return render(request, "new_post.html", {"form": form,})

@login_required
def delete_post(request, post_id):
  post = Post.objects.get(pk=post_id)
  # TODO: If user making request is author, they should also be allowed to delete

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
def toggle_like_post(request, post_id):
  post = Post.objects.get(pk=post_id)
  liker = request.user

  if(Like.objects.filter(post=post, liker=liker).exists()):
    Like.objects.get(post=post, liker=liker).delete()
  else:
    new_like = Like.objects.create(liker=liker, post=post)
    new_like.save()

  return post_detail(request, post_id)
    
  
def muted(request):
  return render(request, "muted.html", { 'logged_in_as': request.user.username })