from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
from django.core.cache import cache as default_cache

class MyThrottle(SimpleRateThrottle):
    scope = "x1"

    # 访问频率 5分钟1次
    THROTTLE_RATES = {"x1": "5/m"}

    cache = default_cache

    def get_cache_key(self, request, view):
        if request.user:
            ident = request.user.pk  # 用户ID
        else:
            ident = self.get_ident(request)  # 获取请求用户IP（去request中找请求头）

        return self.cache_format % {'scope': self.scope, 'ident': ident}

class IpThrottle(SimpleRateThrottle):
    scope = "ip"
    cache = default_cache

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)  # 获取请求用户IP（去request中找请求头）
        return self.cache_format % {'scope': self.scope, 'ident': ident}

class UserThrottle(SimpleRateThrottle):
    scope = "user"
    cache = default_cache

    def get_cache_key(self, request, view):
        ident = request.user.pk  # 用户ID
        return self.cache_format % {'scope': self.scope, 'ident': ident}


