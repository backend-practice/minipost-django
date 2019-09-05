from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostList.as_view(), name='list'),
    path('<int:pk>/', views.PostDetail.as_view(), name='detail'),
    path('<int:post_id>/comments/', views.CommentList.as_view(), name='comment-list'),
    path('<int:post_id>/comments/<int:pk>/', views.CommentDetail.as_view(), name='comment-detail'),
    path('<int:pk>/like/', views.PostLike.as_view(), name='like'),
    # path('feed/', views.PostFeed.as_view(), name='feed'),
]
