import datetime
import uuid

from django.utils import timezone
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

# serializers.Serializer 方式
# class DepartSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     count = serializers.IntegerField()

# serializers.ModelSerializer 方式
class DepartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Depart
        fields = "__all__"

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

# 可仅针对tag序列化
class Depart(serializers.ModelSerializer):
    class Meta:
        models = models.Depart
        fields = "__all__"

# 序列化类
class UserSerializer(serializers.ModelSerializer):
    gender_text = serializers.CharField(source="get_gender_display")

    # 展示外键关联内容
    # 可通过序列化类实现
    # depart = Depart()  如果对象是多个：Depart(many=True)
    depart = serializers.CharField(source="depart.title")

    # 时间序列化器
    ctime = serializers.DateTimeField(format="%Y-%m-%d")

    # 自定义序列化
    xxx = serializers.SerializerMethodField()

    class Meta:
        model = models.UserInfo2
        # fields = "__all__"
        fields = ["name", "age", "gender", "gender_text", "depart", "ctime", "xxx"]

    def get_xxx(self, obj):

        # [Tag对象,.....]
        result = []
        queryset = obj.tags.all()
        print(queryset)
        for tag in queryset:
            result.append({"id": tag.id, "caption":tag.caption})

        return result

class UserView2(APIView):
    # 不需要认证，直接访问即可
    authentication_classes = []

    def get(self, request, *args, **kwargs):

        models.UserInfo2.objects.all().update(ctime=timezone.now())

        # 1.获取数据
        queryset = models.UserInfo2.objects.all()
        # 2.序列化
        ser = UserSerializer(instance=queryset, many=True)
        # 3.返回
        content = {"status": True, "data": ser.data}
        return Response(content)


class DepartSerializer2(serializers.Serializer):
    # required 是否为必填项
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class DepartView2(APIView):

    def post(self, request, *args, **kwargs):
        # 1.获取原始数据
        # request.data

        # 2.校验
        ser = DepartSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data)
        else:
            print(ser.errors)

        return Response("...")




