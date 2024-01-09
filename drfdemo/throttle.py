from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
from django.core.cache import cache as default_cache

class MyThrottle(SimpleRateThrottle):
    scope = "xxx"

    # 访问频率 5分钟1次
    THROTTLE_RATES = {"xxx": "5/m"}

    cache = default_cache

    def get_cache_key(self, request, view):
        if request.user:
            ident = request.user.pk  # 用户ID
        else:
            ident = self.get_ident(request)  # 获取请求用户IP（去request中找请求头）

        return self.cache_format % {'scope': self.scope, 'ident': ident}

