from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Post

# Create your views here.
def index(request):
  posts = Post.objects.order_by("-created_at")
  context = { 'posts': posts, }
  return render(request, 'browse/index.html', context)

def post_detail(request, post_id):
  post = get_object_or_404(Post, pk=post_id)
  return render(request, "browse/post_detail.html", {"post": post})

def user_detail(request, username):
  return HttpResponse("You're looking at %s's posts." % username)