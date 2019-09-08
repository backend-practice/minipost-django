import os
import time
from enum import Enum, unique

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    following = models.ManyToManyField('self', through='Following', related_name='followers', symmetrical=False)


@unique
class Gender(Enum):
    """
    性别
    UNKNOWN: 未知
    MALE: 男性
    FEMALE: 女性
    """
    UNKNOWN = 0
    MALE = 1
    FEMALE = 2


def avatar_image_path(instance, filename):
    """
    图片上传路径： avatars/{id+timestamp}.{ext}
    """
    target = str(instance.user.id) + '-' + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    return os.path.join('avatars', '%s%s' % (target, os.path.splitext(filename)[1]))


class Profile(models.Model):
    """
    nickname: 昵称
    gender: 性别
    avatar: 用户上传头像
    """
    GENDER_CHOICE = (
        (Gender.UNKNOWN.value, _('Unknown')),
        (Gender.MALE.value, _('Male')),
        (Gender.FEMALE.value, _('Female')),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=64, blank=True, unique=True)
    gender = models.SmallIntegerField(choices=GENDER_CHOICE, default=Gender.UNKNOWN.value)
    avatar = models.ImageField(blank=True, upload_to=avatar_image_path)

    def __str__(self):
        return 'Profile<%d, %s, %d>' % (self.user.id, self.nickname, self.gender)


class Following(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_relationship')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_relationship')
    time_followed = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return '%d, %d, %s' % (self.from_user.id, self.to_user.id, self.time_followed)
