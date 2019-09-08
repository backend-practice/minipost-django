from django.contrib.auth import get_user_model
from posts.serializers import PostSerializer
from rest_framework import filters, generics
from rest_framework.generics import get_object_or_404

from users.serializers import UserPublicSerializer, UserSerializer

User = get_user_model()


class UserList(generics.ListCreateAPIView):
    """
    get:
    获取User列表

    post:
    创建用户
    """
    queryset = User.objects.all().order_by('date_joined')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserSerializer
        return UserPublicSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    get:
    获取指定User信息
    """
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer


class UserFollowingList(generics.ListAPIView):
    """
    get:
    获取用户的关注列表
    """
    serializer_class = UserPublicSerializer

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['pk'])
        return user.following.all().order_by('-follower_relationship__time_followed')


class UserFollowerList(generics.ListAPIView):
    """
    get:
    获取用户的粉丝列表
    """
    serializer_class = UserPublicSerializer

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['pk'])
        return user.followers.all().order_by('-following_relationship__time_followed')


class UserPostList(generics.ListAPIView):
    """
    get:
    获取用户的Post列表
    """
    serializer_class = PostSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['time_created']
    ordering = ['-time_created']

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['pk'])
        return user.posts.all()
