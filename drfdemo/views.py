from django.http import JsonResponse

from rest_framework.response import Response

# Create your views here.
def auth(request):
    return JsonResponse({'status': True, 'message': "success"})


def login(request):
    return Response({'status': True, 'message': "success"})
