from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'), # home page/index
  path('p/<uuid:post_id>/', views.post_detail, name='post_detail'), # view details about an individual post
  path('u/<str:username>/', views.user_detail, name='user_detail'), # view details about an individual user
  path('new/', views.new_post, name='new_post'), # create a new post
  path('delete_post/<uuid:post_id>', views.delete_post, name='delete_post'), # delete a post
  path('muted/', views.muted, name='muted'), # user is redirected to this page if they are muted and cannot post
  path('toggle_like_post/<uuid:post_id>', views.toggle_like_post, name='toggle_like_post') # like/unlike a post
]