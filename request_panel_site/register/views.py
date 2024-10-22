from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, HttpResponse, redirect
from .models import TelegramUser 
import json
from icecream import ic
from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import (
    NotTelegramDataError,TelegramDataIsOutdatedError,)
import pandas as pd

from request_panel_site.settings import TELEGRAM_BOT_TOKEN 

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

    # Create or update the user
    user, created = TelegramUser.objects.update_or_create(
        id=user_id,
        defaults={
            'first_name': first_name,
            'username': username,
            'photo_url': photo_url,})
    
    print('user_created')
    return user, created  # Returns the user instance and a boolean indicating if it was created

def login_authentication(request):
    if request.method == "GET":
        if request.GET.get('hash'):
            ic('hash was found')
            data = request.GET
            
            try:
                result = verify_telegram_authentication(bot_token=TELEGRAM_BOT_TOKEN, request_data=request.GET)

            except TelegramDataIsOutdatedError:
                return HttpResponse('Authentication was received more than a day ago.')

            except NotTelegramDataError:
                return HttpResponse('The data is not related to Telegram!')

            if data.get('username')[0] in (get_staff_members.admins.values, get_staff_members.managers.values):
                # validation of manager ixist in db
                save_telegram_user(data)
                return ('main_panel')

    return redirect('login')


def get_staff_members():
    sheet_id = "1dJl-3iTEpBWXJjkX183L0sx2FlQCVm4Ci0bc1iMGYhI"
    gid = "1496823880"
    excel = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx&gid={gid}"
    data = pd.read_excel(excel)
    data.columns = ['admins', 'managers','another']
    return data