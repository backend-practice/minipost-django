from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)  # 转发的post删除，会成为非转发post，有问题
    content = models.CharField(max_length=1024)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    time_created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_liked = models.DateTimeField(auto_now_add=True)
