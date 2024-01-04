import random

from rest_framework.permissions import BasePermission

# 权限组件
class UserPermission(BasePermission):
    message = {"code": 1003, "msg": "无权限访问"}

    def has_permission(self, request, view):
        # 获取请求中的数据，然后进行校验....
        if request.user.role == 3:
            return True
        return False

class ManagerPermission(BasePermission):
    message = {"code": 1003, "msg": "无权限访问"}

    def has_permission(self, request, view):
        # 获取请求中的数据，然后进行校验....
        if request.user.role == 2:
            return True
        return False

class BossPermission(BasePermission):
    message = {"code": 1003, "msg": "无权限访问"}

    def has_permission(self, request, view):
        # 获取请求中的数据，然后进行校验....
        if request.user.role == 1:
            return True
        return False
