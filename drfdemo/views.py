from django.http import JsonResponse
from rest_framework.decorators import api_view

from rest_framework.response import Response

# Create your views here.
from rest_framework.views import APIView

from rest_framework.response import Response


def auth(request):
    return JsonResponse({'status': True, 'message': "success"})

@api_view(["GET"])
def login(request):
    return Response({'status': True, 'message': "success"})
class InfoView(APIView):

    def get(self, request):
        return Response({'status': True, 'message': "success"})


class UserView(APIView):
    def get(self, request):
        return Response({'status': True, 'message': "GET"})

    def post(self, request):
        return Response({'status': True, 'message': "POST"})

    def put(self, request):
        return Response({'status': True, 'message': "PUT"})


    def delete(self, request):
        return Response({'status': True, 'message': "DELETE"})

class DemoView(APIView):

    def get(self, request):
        return Response({'status': True, 'message': "success"})

