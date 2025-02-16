"""
URL configuration for zeus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import RedirectView

from browse.views import index, post_detail, user_detail, new_post, account_settings, delete_post, toggle_like_post, post_reply, delete_own_user, muted
from register.views import register

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('browse/', index, name='index'),
    path('p/<uuid:post_id>/', post_detail, name='post_detail'), # view details about an individual post
    path('u/<str:username>/', user_detail, name='user_detail'), # view details about an individual user
    path('new/', new_post, name='new_post'), # create a new post
    path('delete_post/<uuid:post_id>', delete_post, name='delete_post'), # delete a post
    path('muted/', muted, name='muted'), # user is redirected to this page if they are muted and cannot post
    path('toggle_like_post/<uuid:post_id>/<str:sender>', toggle_like_post, name='toggle_like_post'), # like/unlike a post
    path('post_reply/<uuid:post_id>/<str:content>', post_reply, name='post_reply'), # post a reply to a post
    path('delete_own_user/', delete_own_user, name='delete_own_user'), # delete own user
    path('account_settings/', account_settings, name='account_settings'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('register/', register, name='register')
]
