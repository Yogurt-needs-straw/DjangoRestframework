import random

from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):
    def has_permission(self, request, view):
        # 获取请求中的数据，然后进行校验....
        v1 = random.randint(1,3)
        if v1 == 2:
            return True
        return False