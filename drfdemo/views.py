import uuid
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from drfdemo import models
from drfdemo.per import MyPermission
from drfdemo.view_check_permissions import CheckApiView


class LoginView(APIView):
    # 不需要认证，直接访问即可
    authentication_classes = []

    # 重新定义 权限校验
    permission_classes = []

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

        # 3.用户正确
        token = str(uuid.uuid4())
        user_object.token = token
        user_object.save()

        return Response({"code": 2001, "msg": token})


class UserView(APIView):
    # 需要认证
    # authentication_classes = []

    def get(self, request):
        print(request.user, request.auth)
        return Response("UserView")

    def post(self, request):
        print(request.user, request.auth)
        return Response("UserViewPost")

# 使用自定义权限校验
class OrderView(CheckApiView):

    # 权限组件的应用
    permission_classes = [MyPermission, ]

    def get(self, request):
        print(request.user, request.auth)
        return Response("OrderView")



