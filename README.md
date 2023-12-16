# DjangoRestframework

- 项目部署

- 前后端分离

  - 程序角度：1个django程序，接收请求+处理+HTML模板+用户返回
  - 2个程序
    - 前端：vue.js/react.js/angular.js
    - 后端：django + django restframework

  - 专业度角度：
    - 前端 前端代码 + 部署 + 版本管理 + ajax请求获取
    - 后端 API 

  

APP 或 微信小程序

- 前端：APP或微信小程序
- 后端：API



## Restframework



### 官方文档

[Home - Django REST framework (django-rest-framework.org)](https://www.django-rest-framework.org/)



### 安装

```bash
pip install djangorestframework
```

### 注册

settings.py

```python
INSTALLED_APPS = [
    "rest_framework"
]
```



## 接口调试工具

postman

apifox



## 初步编写API

- 基于django实现

- 基于drf实现

  

### 路由

```python
path('auth/', views.auth),
```



### 视图

```python
def auth(request):
    return JsonResponse({'status': True, 'message': "success"})
```



## FBV 和 CBV

- 现象
- 本质相同



**POST请求 免除CSRF token校验**

```python
@csrf_exempt
def info(request):
	pass
```



## CBV -> (DRF) -> dispath

```python
path('user/<int:pk>', views.UserView.as_view())

def get(self, request, pk):
```

- 请求对象和参数

  django的request对象

  ​	request.method

  ​	request.GET

  ​	request.POST

​	drf 中的 request 参数，又一层封装

​			# request._request.GET

​			# request._request.POST

​			# request._request.method

​	class Request:

​			def \__init__(self, request,......):

​					self._request = request

​					self.....



## 前后端分离

- 不分离
  - 后台系统 & 用户量少
- 前后端分离
  - 用户系统 & 专业分工



## restframework匿名用户报错

> django 纯净版

```python
# 源码 restframework request.py 中 
def _not_authenticated(self):
    if api_settings.UNAUTHENTICATED_USER:
        self.user = api_settings.UNAUTHENTICATED_USER()
    else:
        self.user = None
```

> 解决

settings.py

```python
REST_FRAMEWORK = {
    "UNAUTHENTICATED_USER": None,
    # "UNAUTHENTICATED_TOKEN": None,
}

```



## Request 对象

- OOP知识

```python
对象的封装
class Foo(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    # 当通过对象访问一个不存在的东西，getattr会执行
    def __getattr__(self, item):
        print(item)
		return 123
    
    # 只要执行 对象.xxx都会执行 __getattribute__
    # 对象中有值，返回
    # 对象中没有值，报错
    def __getattribute__(self, item):
        print("-->", item)
        return 999
    
    # drf中request方法
    # 对象中有的成员，不会触发
    # 对象中无的成员，会触发
    def __getattr__(self, attr):
        # attr = "yyy"
        try:
            return getattr(self._request, attr) # self._request.yyy
        except AttributeError:
            return self.__getattribute__(attr)
```



- drf请求流程
  - *args, **kwargs


 
