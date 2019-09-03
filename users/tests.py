# from django.urls import reverse
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Gender, Profile


class UserListViewTests(APITestCase):
    def test_list_no_user(self):
        """
        没有User时返回空列表
        """
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['results'], [])

    def test_list_user(self):
        """
        返回只有一个User的列表
        """
        user = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password',
        )
        profile = Profile.objects.create(
            user=user,
            nickname='nickname',
            gender=Gender.MALE.value,
        )
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], user.id)
        self.assertEqual(response.data['results'][0]['username'], user.username)
        self.assertEqual(response.data['results'][0]['nickname'], profile.nickname)
        self.assertEqual(response.data['results'][0]['gender'], profile.gender)
        self.assertIsNone(response.data['results'][0]['avatar'])
        # 隐私信息，不会返回
        self.assertTrue('password' not in response.data['results'][0])
        self.assertTrue('email' not in response.data['results'][0])

    def test_create_user(self):
        """
        创建User
        """
        user_data = {
            'username': 'user1',
            'email': 'user1@example.com',
            'password': 'password',
            'nickname': 'nickname',
            'gender': Gender.MALE.value,
        }
        response = self.client.post(reverse('users:list'), user_data)
        # 测试数据库
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        user = User.objects.get()
        profile = Profile.objects.get()
        self.assertEqual(user.username, user_data['username'])
        self.assertEqual(user.email, user_data['email'])
        self.assertEqual(profile.nickname, user_data['nickname'])
        self.assertEqual(profile.gender, user_data['gender'])
        self.assertNotEqual(user.password, user_data['password'])  # password不应明文存储
        # 测试接口返回值
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user_data['username'])
        self.assertEqual(response.data['email'], user_data['email'])
        self.assertEqual(response.data['nickname'], user_data['nickname'])
        self.assertEqual(response.data['gender'], user_data['gender'])
        self.assertTrue('password' not in response.data)


class UserDetailViewTests(APITestCase):
    def test_get_user_that_not_exist(self):
        """
        User不存在时，查看用户信息
        """
        response = self.client.get(reverse('users:detail', args=(1,)), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Not found.'})

    def test_get_user(self):
        """
        匿名用户查看指定User信息
        """
        user = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password',
        )
        profile = Profile.objects.create(
            user=user,
            nickname='nickname',
            gender=Gender.MALE.value,
        )
        response = self.client.get(reverse('users:detail', args=(user.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['nickname'], profile.nickname)
        self.assertEqual(response.data['gender'], profile.gender)
        self.assertIsNone(response.data['avatar'])
        # 隐私信息，不会返回
        self.assertTrue('password' not in response.data)
        self.assertTrue('email' not in response.data)
