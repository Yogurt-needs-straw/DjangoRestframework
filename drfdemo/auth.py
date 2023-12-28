from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from drfdemo import models

# query中携带token
class QueryParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 做用户认证：
        # 1.读取请求传递的token
        # 2.校验合法性
        # 3.返回值
        #  3.1 返回元组(request.user,request.auth)
        #  3.2 抛出异常 认证失败
        #  3.3 返回None  多个认证类[类1,类2]

        token = request.query_params.get("token")
        if not token:
            return

        user_object = models.UserInfo.objects.filter(token=token).first()
        if user_object:
            return user_object, token

        return

    def authenticate_header(self, request):
        return "API"

# Header中携带token
class HeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 做用户认证：
        # 1.读取请求传递的token
        # 2.校验合法性
        # 3.返回值
        #  3.1 返回元组(request.user,request.auth)
        #  3.2 抛出异常 认证失败
        #  3.3 返回None  多个认证类[类1,类2]

        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            return

        user_object = models.UserInfo.objects.filter(token=token).first()


        if user_object:
            return user_object, token

        return

    def authenticate_header(self, request):
        return "API"

class NoAuthentication(BaseAuthentication):
    def authenticate(self, request):
        raise AuthenticationFailed({"status": False, 'msg': "认证失败"})

    def authenticate_header(self, request):
        return "API"