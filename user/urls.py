from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.CurrentUser.as_view(), name='current-user'),
    path('following/', views.CurrentUserFollowingList.as_view(), name='current-user-following-list'),
    path('following/<int:user_id>/', views.CurrentUserFollowingDetail.as_view(), name='current-user-following-detail'),
    path('followers/', views.CurrentUserFollowerList.as_view(), name='current-user-follower-list'),
    path('posts/', views.CurrentUserPostList.as_view(), name='current-user-post-list'),
]
