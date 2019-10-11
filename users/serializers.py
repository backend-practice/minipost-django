from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from posts.models import Post

from .models import Following, Profile

User = get_user_model()


class UserBaseSerializer(serializers.ModelSerializer):
    """
    序列化用户User，只包含基本信息，不包含隐私信息和关联信息
    """
    nickname = serializers.CharField(source='profile.nickname')
    gender = serializers.ChoiceField(source='profile.gender', choices=Profile.GENDER_CHOICE)
    avatar = serializers.ImageField(source='profile.avatar', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'gender', 'avatar')


class UserPublicSerializer(UserBaseSerializer):
    """
    序列化用户User，不包含隐私信息，包含关联信息
    """
    posts_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'nickname', 'gender', 'avatar', 'posts_count', 'following_count', 'followers_count'
        )

    def get_posts_count(self, obj):
        user = self.context['request'].user
        if not (user and user.is_authenticated):
            return 0
        return Post.objects.filter(owner=user).count()

    def get_following_count(self, obj):
        user = self.context['request'].user
        if not (user and user.is_authenticated):
            return 0
        return user.following.count()

    def get_followers_count(self, obj):
        user = self.context['request'].user
        if not (user and user.is_authenticated):
            return 0
        return user.followers.count()


class UserSerializer(UserPublicSerializer):
    """
    序列化用户User，包含隐私信息，用于读写用户信息
    """
    nickname = serializers.CharField(
        source='profile.nickname',
        validators=[UniqueValidator(queryset=Profile.objects.all())],
    )
    gender = serializers.ChoiceField(source='profile.gender', choices=Profile.GENDER_CHOICE)
    avatar = serializers.ImageField(source='profile.avatar', read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'nickname', 'gender', 'avatar', 'password', 'posts_count', 'following_count',
            'followers_count',
        )

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            Profile.objects.create(user=user, **profile_data)
            return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        try:
            profile = instance.profile
        except Profile.DoesNotExist:
            # 通过接口创建的User，对应的Profile自动被创建
            profile = Profile()
            profile.user = instance
        profile.nickname = profile_data.get('nickname', profile.nickname)
        profile.gender = profile_data.get('gender', profile.gender)
        with transaction.atomic():
            instance.save()
            profile.save()
        return instance


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = '__all__'

    def validate(self, attrs):
        if attrs['from_user'] == attrs['to_user']:
            raise serializers.ValidationError('You can\'t follow yourself.')
        return attrs
