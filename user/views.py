from django.contrib.auth import get_user_model
from posts.serializers import PostSerializer
from rest_framework import filters, generics, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from users.models import Following
from users.serializers import (
    FollowingSerializer, UserPublicSerializer, UserSerializer,
)

User = get_user_model()


class CurrentUser(generics.RetrieveUpdateAPIView):
    """
    get:
    获取当前登录用户的信息

    put:
    修改当前登录用户的信息
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CurrentUserFollowingList(generics.ListAPIView):
    """
    get:
    获取当前登录用户的关注列表
    """
    serializer_class = UserPublicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.following.all().order_by('-follower_relationship__time_followed')


class CurrentUserFollowingDetail(generics.GenericAPIView,
                                 mixins.CreateModelMixin,
                                 mixins.DestroyModelMixin):
    """
    post:
    关注其他用户

    delete:
    取消关注其他用户
    """
    # queryset = Following.objects.all()  # TODO: create need this?
    serializer_class = FollowingSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        to_user = get_object_or_404(User, id=self.kwargs['user_id'])
        return get_object_or_404(
            Following,
            from_user=self.request.user,
            to_user=to_user,
        )

    def post(self, request, *args, **kwargs):
        request.data['from_user'] = self.request.user.id
        request.data['to_user'] = self.kwargs['user_id']
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, args, kwargs)


class CurrentUserFollowerList(generics.ListAPIView):
    """
    get:
    获取当前登录用户的粉丝列表
    """
    serializer_class = UserPublicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.followers.all().order_by('-following_relationship__time_followed')


class CurrentUserPostList(generics.ListAPIView):
    """
    get:
    获取当前登录用户的Post列表
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['time_created']
    ordering = ['-time_created']

    def get_queryset(self):
        return self.request.user.posts.all()
