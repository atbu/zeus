from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .forms import NewPostForm
from .models import Post

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
  return render(request, "browse/post_detail.html", {"post": post,})

def user_detail(request, username):
  user = get_object_or_404(get_user_model(), username=username)
  posts = Post.objects.filter(author__username=username)
  context = {
    "user": user,
    "posts": posts,
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