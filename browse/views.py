from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Post

# Create your views here.
def index(request):
  posts = Post.objects.order_by("-created_at")
  return render(request, 'browse/index.html', {'posts': posts,})

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