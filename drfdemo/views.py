from django.http import JsonResponse
from rest_framework.decorators import api_view

from rest_framework.response import Response

# Create your views here.
from rest_framework.views import APIView

from rest_framework.response import Response


def home(request):
    return JsonResponse({'status': True, 'message': "success"})


class UserView(APIView):
    def get(self, request):
        return Response("返回成功")

