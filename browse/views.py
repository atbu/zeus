# from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
  return HttpResponse("Welcome to the browse index.")

def detail(request, post_id):
  return HttpResponse("You're looking at post %s." % post_id)