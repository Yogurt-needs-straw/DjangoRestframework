from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from drfdemo import models


class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 做用户认证：
        # 1.读取请求传递的token
        # 2.校验合法性
        # 3.返回值
        #  3.1 返回元组(request.user,request.auth)
        #  3.2 抛出异常 认证失败
        #  3.3 返回None  多个认证类[类1,类2]

        token = request._request.GET.get("token")
        token_2 = request.query_params.get("token")

        if token:
            return "123", token
        raise AuthenticationFailed({"code": 400, "error": "认证失败"})

    def authenticate_header(self, request):
        return "API"

class LoginView(APIView):
    # 不需要认证，直接访问即可
    authentication_classes = []

    def get(self, request):
        return Response("返回成功")

    def post(self, request):
        # 1.接收用户提交的用户名和密码 JSON
        # print(request._request.body)
        user = request.data.get("username")
        pwd = request.data.get("password")

        # 2.数据库校验
        user_object = models.UserInfo.objects.filter(username=user, password=pwd).first()
        if not user_object:
            return Response({"code": 1001, "msg": "用户名密码错误"})


        return Response("LoginView")

class UserView(APIView):
    # 需要认证
    authentication_classes = [MyAuthentication,]

    def get(self, request):
        print(request.user, request.auth)
        return Response("UserView")


class OrderView(APIView):

    authentication_classes = [MyAuthentication, ]

    def get(self, request):
        print(request.user, request.auth)
        return Response("OrderView")

