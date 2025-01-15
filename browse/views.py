from django.http import HttpResponse
from django.shortcuts import render
from .models import Post

# Create your views here.
def index(request):
  posts = Post.objects.order_by("-created_at")
  context = { 'posts': posts, }
  return render(request, 'browse/index.html', context)

def post_detail(request, post_id):
  return HttpResponse("You're looking at post %s." % post_id)

def user_detail(request, username):
  return HttpResponse("You're looking at %s's posts." % username)