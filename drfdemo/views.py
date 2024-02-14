import uuid
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from rest_framework.negotiation import DefaultContentNegotiation
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning, AcceptHeaderVersioning
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from drfdemo import models
from drfdemo.per import BossPermission, UserPermission, ManagerPermission
from drfdemo.throttle import MyThrottle, IpThrottle, UserThrottle
from drfdemo.view_check_permissions import CheckApiView


class LoginView(APIView):

    # 添加限流组件
    throttle_classes = [IpThrottle, ]

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
        # print(user_object)
        if not user_object:
            return Response({"code": 1001, "msg": "用户名密码错误"})

        # 3.用户正确
        token = str(uuid.uuid4())
        user_object.token = token
        user_object.save()

        return Response({"code": 2001, "msg": token})


class UserView(CheckApiView):
    # 经理 或 总监 或 用户 可以访问
    permission_classes = [BossPermission, ManagerPermission, UserPermission]

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

    # 经理 或 总监 可以访问

    # 权限组件的应用
    permission_classes = [BossPermission, ManagerPermission]

    def get(self, request):
        print(request.user, request.auth)
        return Response("OrderView")


class AvatarView(CheckApiView):
    # 添加限流组件
    throttle_classes = [UserThrottle, ]

    # 总监 或 员工 可以访问
    permission_classes = [BossPermission, UserPermission]

    def get(self, request):
        print(request.user, request.auth)
        return Response("AvatarView")


class HomeView(APIView):

    # 不需要认证，直接访问即可
    authentication_classes = []

    # 配置文件 VERSION_PARAM
    # http://127.0.0.1:8000/home/?xxx
    versioning_class = QueryParameterVersioning

    def get(self, request):

        print(request.version)

        # 反向生成url
        # http://127.0.0.1:8000/home/?version=v1
        url = request.versioning_scheme.reverse('home', request=request)
        print(url)

        # self.dispatch()

        return Response("...")

    # 所有的解析器
    parser_classes = [JSONParser, FormParser]

    # 根据请求，匹配对应的解析器; 寻找渲染器
    content_negotiation_class = DefaultContentNegotiation

    def post(self, request, *args, **kwargs):
        # 当调用request.data时就会触发解析的动作。
        print(request.data)

        return Response("OK")

class HomeToView(APIView):
    # 不需要认证，直接访问即可
    authentication_classes = []

    # 可在settings中设置
    # versioning_class = URLPathVersioning

    def get(self, request, version):
        print(request.version)

        return Response("...")


class HomeTiView(APIView):
    # 不需要认证，直接访问即可
    authentication_classes = []

    versioning_class = AcceptHeaderVersioning

    def get(self, request, *args, **kwargs):
        print(request.version)

        return Response("...")


class ImgView(APIView):

    # 所有的解析器
    # MultiPartParser 只支持文件上传
    parser_classes = [MultiPartParser, ]

    def post(self, request, *args, **kwargs):
        # 当调用request.data时就会触发解析的动作。
        print(request.data)

        return Response("OK")


class DepartSerializer(serializers.Serializer):
    title = serializers.CharField()
    count = serializers.IntegerField()

class DepartView(APIView):
    # 不需要认证，直接访问即可
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        # 1.数据库中获取数据
        queryset = models.Depart.objects.all()

        # 2.转换为JSON格式
        # queryset多个结果 添加many属性
        ser = DepartSerializer(instance=queryset, many=True)
        print(ser.data)

        # 3.返回给用户
        content = {"status": True, "data": ser.data}
        return Response(content)

