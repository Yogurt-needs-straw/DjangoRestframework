import datetime
import uuid

from django.core.validators import RegexValidator
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from rest_framework.negotiation import DefaultContentNegotiation
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning, AcceptHeaderVersioning
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, exceptions

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
    # username = serializers.CharField(required=True)
    # password = serializers.CharField(required=True)

    title = serializers.CharField(required=True, max_length=20, min_length=6)
    order = serializers.IntegerField(required=False, max_value=100, min_value=10)
    level = serializers.ChoiceField(choices=[("1", "高级"), (2, "中级")])

    email = serializers.CharField(validators=[RegexValidator(message="邮箱格式错误")])

    # 钩子函数 校验数据 对单个数据进行校验
    def validate_email(self, value):
        if len(value) > 6:
            raise exceptions.ValidationError("字典钩子校验失败")
        return value

    # 整体钩子
    def validate(self, attrs):
        print("validate=", attrs)
        # api_setting.NON_FIELD_ERRORS_KEY
        raise exceptions.ValidationError("全局钩子校验失败")

class DepartModelSerializer2(serializers.ModelSerializer):
    class Meta:
        model = models.Depart
        fiels = ["title", "order", "count"]

        # 校验条件
        extra_kwargs = {
            "title": {"max_value": 5, "min_value": 1},
            "order": {"min_value": 5}
        }



class DepartView2(APIView):
    # 不需要认证，直接访问即可
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        # 1.获取原始数据
        # request.data

        # 2.校验
        # ser = DepartSerializer(data=request.data)
        ser = DepartModelSerializer2(data=request.data)
        if ser.is_valid():
            print("视图", ser.validated_data)
        else:
            print("视图", ser.errors)

        # ser = DepartSerializer(data=request.data)
        # ser.is_valid(raise_exception=True) # 成功, 抛出异常 raise ValidationError(self.error)
        return Response("...")


class UsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo2
        fields = ["name", "age", "gender", "depart"]

    # 钩子函数 对单个选项校验
    def validate_depart(self, value):
        if value.id > 1:
            return value
        raise exceptions.ValidationError("部门错误")

class UsView(APIView):
    # 不需要认证，直接访问即可
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        # 1.获取原始数据
        # request.data

        # 2.校验
        ser = UsModelSerializer(data=request.data)
        if ser.is_valid():
            print("视图", ser.validated_data)
            ser.save()
        else:
            print("视图", ser.errors)

        return Response("...")

# 自定义一个字段
class NbCharField(serializers.IntegerField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name

        super().__init__(**kwargs)

    def bind(self, field_name, parent):
        # The method name default to 'get_{field_name}'
        if self.method_name is None:
            self.method_name = 'xget_{field_name}'.format(field_name=field_name)  #'get_gender'

        super().bind(field_name, parent)

    def get_attribute(self, instance):
        method = getattr(self.parent, self.method_name)
        return method(instance)

    def to_representation(self, value):
        return str(value)

class NbModelSerializer(serializers.ModelSerializer):
    gender = NbCharField()

    class Meta:
        model = models.NbUser
        fields = ["id", "name", "age", "gender"]
        extra_kwargs = {
            "id": {"read_only": True},
            # "gender": {"write_only": True},
        }

    def xget_gender(self, obj):
        return obj.get_gender_display()


class NbView(APIView):
    # 不需要认证，直接访问即可
    authentication_classes = []

    def post(self, reqest, *args, **kwargs):
        ser = NbModelSerializer(data=reqest.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            return Response(ser.errors)


class SbView:
    # 不需要认证，直接访问即可
    authentication_classes = []

    def post(self, reqest, *args, **kwargs):
        ser = SbModelSerializer(data=reqest.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            return Response(ser.errors)
