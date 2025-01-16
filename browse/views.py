from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .forms import NewPostForm
from .models import Post, ModeratorAction

# Create your views here.
def index(request):
  posts = Post.objects.order_by("-created_at")

  logged_in_as = ""
  if(request.user.is_authenticated):
    logged_in_as = request.user.username

  context = {
    'posts': posts,
    'logged_in_as': logged_in_as,
  }

  return render(request, 'browse/index.html', context)

def post_detail(request, post_id):
  post = get_object_or_404(Post, pk=post_id)

  logged_in_as = ""
  if(request.user.is_authenticated):
    logged_in_as = request.user.username

  context = {
    "post": post,
    "logged_in_as": logged_in_as,
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
    Post.objects.filter(id=post_id).delete()
    ModeratorAction.create(moderator=request.user, type='deletion', post=Post.objects.get(id=post_id))
    return HttpResponseRedirect('/')