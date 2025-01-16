from django.contrib import admin
from .models import Post, Like, Action

# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Action)