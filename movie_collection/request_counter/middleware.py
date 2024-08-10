from django.core.cache import cache

class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Increment the request count
        current_count = cache.get('request_count', 0)
        cache.set('request_count', current_count + 1)
        response = self.get_response(request)
        return response