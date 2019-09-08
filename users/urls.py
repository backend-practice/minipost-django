from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserList.as_view(), name='list'),
    path('<int:pk>/', views.UserDetail.as_view(), name='detail'),
    path('<int:pk>/following/', views.UserFollowingList.as_view(), name='user-following-list'),
    path('<int:pk>/followers/', views.UserFollowerList.as_view(), name='user-follower-list'),
    path('<int:pk>/posts/', views.UserPostList.as_view(), name='user-post-list'),
]
