from rest_framework.views import APIView


class CheckApiView(APIView):
    # 重写权限校验方法
    # 实现自定义权限校验
    # 实现多个条件选择性校验通过
    def check_permissions(self, request):
        no_permission_objects = []
        for permission in self.get_permissions():
            if permission.has_permission(request, self):
                return
            else:
                no_permission_objects.append(permission)
        else:
            self.permission_denied(
                request,
                message=getattr(no_permission_objects[0], 'message', None),
                code=getattr(no_permission_objects[0], 'code', None),
            )

