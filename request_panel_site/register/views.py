from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, HttpResponse
import datetime
import json



def login_page(request):
    content = render(request, 'login_page.html').content
    response = HttpResponse(content)
    response.headers['Content-Security-Policy'] = "default-src 'self' https://core.telegram.org https://oauth.telegram.org; frame-ancestors 'self' https://core.telegram.org https://oauth.telegram.org"
    response.headers['X-Frame-Options'] = 'ALLOW-FROM https://core.telegram.org https://oauth.telegram.org'
    return response


@require_http_methods(['POST'])
def login_view(request):
    try:
        user_data = json.loads(request.body)
        print(user_data)  # Process the user's data here
        print('hello world!!@#!@#!@#')
        return JsonResponse({'message': 'Login successful'})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'message': 'Error occurred'})
    

def login_authentication(request):
    ...
