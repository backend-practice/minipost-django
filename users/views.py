from django.contrib.auth.models import User
from rest_framework import generics

from users.serializers import UserPublicSerializer, UserSerializer


class UserList(generics.ListCreateAPIView):
    """
    get:
    获取User列表

    post:
    创建用户
    """
    queryset = User.objects.all()

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
