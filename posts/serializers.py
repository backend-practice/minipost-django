from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.serializers import UserBaseSerializer

from .models import Comment, Like, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """
    序列化Post
    """
    owner = UserBaseSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(source='owner', queryset=User.objects.all())
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    @staticmethod
    def get_likes_count(obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if not (user and user.is_authenticated):
            return False
        return Like.objects.filter(user=user, post=obj.id).exists()


class CommentSerializer(serializers.ModelSerializer):
    """
    序列化Comment
    """
    owner = UserBaseSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(source='owner', queryset=User.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    """
    序列化Like
    """
    user = UserBaseSerializer(read_only=True)

    class Meta:
        model = Like
        fields = '__all__'
