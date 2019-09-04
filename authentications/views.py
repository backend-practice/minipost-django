from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


class Authentications(ObtainAuthToken):
    """
    post:
    登录并创建token

    delete:
    退出登录并删除token
    """

    @staticmethod
    def delete(request):
        """
        删除token，注销登录
        """
        if request.user and request.user.is_authenticated:
            token = Token.objects.get(user=request.user)
            print(token)
            token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
