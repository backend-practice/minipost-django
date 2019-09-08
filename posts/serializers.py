from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.serializers import UserPublicSerializer

from .models import Comment, Like, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """
    序列化Post
    """
    owner = UserPublicSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(source='owner', queryset=User.objects.all())
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    @staticmethod
    def get_like_count(obj):
        return obj.likes.count()


class CommentSerializer(serializers.ModelSerializer):
    """
    序列化Comment
    """
    owner = UserPublicSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(source='owner', queryset=User.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    """
    序列化Like
    """
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Like
        fields = '__all__'
