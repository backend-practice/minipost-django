from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from posts.models import Comment, Like, Post
from posts.permissions import IsOwnerOrReadonly
from posts.serializers import CommentSerializer, PostSerializer


class PostList(generics.ListCreateAPIView):
    """
    get:
    获取post列表

    post:
    创建post
    """
    queryset = Post.objects.all().order_by('-time_created')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        # authenticated
        request.data['owner_id'] = request.user.id
        return self.create(request, *args, **kwargs)


class PostDetail(generics.RetrieveDestroyAPIView):
    """
    get:
    获取post

    delete:
    删除post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadonly]


class CommentList(generics.ListCreateAPIView):
    """
    get:
    获取评论列表

    post:
    创建评论
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_id'])

    def post(self, request, *args, **kwargs):
        # authenticated
        request.data['owner_id'] = request.user.id
        request.data['post'] = self.kwargs['post_id']
        return self.create(request, *args, **kwargs)


class CommentDetail(generics.RetrieveDestroyAPIView):
    """
    get:
    获取评论

    delete:
    删除评论
    """
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadonly]

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_id'])


class PostLike(generics.GenericAPIView):
    """
    post:
    点赞

    delete:
    取消点赞
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        Like.objects.get_or_create(post=post, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        try:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
        except Like.DoesNotExist:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostFeed(generics.ListAPIView):
    """
    get:
    获取关注用户的Post
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(owner__in=self.request.user.following.all())
