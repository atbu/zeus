from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('p/<uuid:post_id>/', views.post_detail, name='post_detail'),
  path('u/<str:username>/', views.user_detail, name='user_detail'),
  path('new/', views.new_post, name='new_post'),
]