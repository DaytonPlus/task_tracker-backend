from django.http import JsonResponse

class EnsureJSONMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ['POST', 'PUT', 'PATCH']:
            if not request.content_type == 'application/json':
                return JsonResponse({'error': 'Invalid Content-Type'}, status=415)
        return self.get_response(request)

