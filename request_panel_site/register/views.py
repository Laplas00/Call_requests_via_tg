from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, HttpResponse, redirect
from .models import TelegramUser 
import json
from icecream import ic



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
    
# --- Telegram authentication

def save_telegram_user(data):
    user_id = int(data.get('id')[0])
    first_name = data.get('first_name')[0]
    username = data.get('username')[0] if data.get('username') else None
    photo_url = data.get('photo_url')[0] if data.get('photo_url') else None
    hash_value = data.get('hash')[0]

    # Create or update the user
    user, created = TelegramUser.objects.update_or_create(
        id=user_id,
        defaults={
            'first_name': first_name,
            'username': username,
            'photo_url': photo_url,
            'hash': hash_value,})
    return user, created  # Returns the user instance and a boolean indicating if it was created

def login_authentication(request):
    if request.method == "GET":
        if request.GET.get('hash'):
            ic('hash was found')
            data = request.GET
            save_telegram_user(data)

    return redirect('main_panel')
    
    ...


from .models import TelegramUser 
from django.utils import timezone

