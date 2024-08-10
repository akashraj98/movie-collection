from django.http import JsonResponse
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response


class RequestCountView(APIView):
    def get(self, request):
        count = cache.get('request_count', 0)
        return Response({"requests": count})

class RequestCountResetView(APIView):
    def post(self, request):
        cache.set('request_count', 0)
        return Response({"message": "request count reset successfully"})