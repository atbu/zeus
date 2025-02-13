from django.contrib import admin
from .models import Post, Like, Action, Mute

# Registers the models under the admin site so they can be managed.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Action)
admin.site.register(Mute)