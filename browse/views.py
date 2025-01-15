# from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# Create your views here.
def index(request):
  posts = Post.objects.order_by("-created_at")
  output = ""
  for p in posts:
    output += "<h3>%s <strong>(by %s)</strong></h3><br />" % p.author.username
  return HttpResponse(output)

def detail(request, post_id):
  return HttpResponse("You're looking at post %s." % post_id)