from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import User


class AuthenticationsViewTests(APITestCase):
    def test_create_token_with_invalid_username_password(self):
        """
        使用无效的用户名密码创建token
        """
        response = self.client.post(
            reverse('authentications:authentications'),
            {'username': 'noneexist', 'password': 'wrong_password'},
        )
        self.assertEqual(Token.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'Unable to log in with provided credentials.')

    def test_create_token_with_valid_username_password(self):
        """
        使用正确的用户名密码创建Token
        """
        username = 'user1'
        password = 'user1password'
        user = User.objects.create_user(username=username, password=password)
        response = self.client.post(
            reverse('authentications:authentications'),
            {'username': username, 'password': password},
        )
        token = Token.objects.get(user=user)
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], token.key)

    def test_delete_with_invalid_token(self):
        """
        使用不正确的token访问删除token
        """
        username = 'user1'
        password = 'user1password'
        user = User.objects.create_user(username=username, password=password)
        token, created = Token.objects.get_or_create(user=user)
        fake_token = '82048ec19bce54f73018a72c5826db692c57c03b'
        if fake_token == token.key:
            fake_token = 'd159247d453c3685f16e1cfe52e38461a72f1cf0'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + fake_token)
        response = self.client.delete(reverse('authentications:authentications'))
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # TODO: Why 401

    def test_delete_token_valid_token(self):
        """
        使用正确的token访问删除token
        """
        username = 'user1'
        password = 'user1password'
        user = User.objects.create_user(username=username, password=password)
        token, created = Token.objects.get_or_create(user=user)
        self.assertEqual(Token.objects.count(), 1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(reverse('authentications:authentications'))
        self.assertEqual(Token.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
