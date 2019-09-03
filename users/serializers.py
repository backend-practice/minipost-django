from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class UserPublicSerializer(serializers.ModelSerializer):
    """
    序列化用户User，不包含隐私信息
    """
    nickname = serializers.CharField(source='profile.nickname')
    gender = serializers.ChoiceField(source='profile.gender', choices=Profile.GENDER_CHOICE)
    avatar = serializers.ImageField(source='profile.avatar', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'gender', 'avatar')


class UserSerializer(UserPublicSerializer):
    """
    序列化用户User，包含隐私信息，用于读写用户信息
    """
    nickname = serializers.CharField(source='profile.nickname')
    gender = serializers.ChoiceField(source='profile.gender', choices=Profile.GENDER_CHOICE)
    avatar = serializers.ImageField(source='profile.avatar', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'gender', 'avatar', 'password')

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        try:
            profile = instance.profile
        except Profile.DoesNotExist:
            # 通过接口创建的User，对应的Profile自动被创建
            profile = Profile()
            profile.user = instance
        profile.nickname = profile_data.get('nickname', profile.nickname)
        profile.gender = profile_data.get('gender', profile.gender)
        profile.save()
        return instance
