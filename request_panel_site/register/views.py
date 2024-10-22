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
    user_id = data.get('id')
    first_name = data.get('first_name')
    username = data.get('username')
    photo_url = data.get('photo_url')

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
        if request.user.is_authenticated:
            print('user is authenticated')
            return redirect('main_panel')

        if request.GET.get('hash'):
            ic('hash was found')
            data = request.GET
            ic(data)
            try:
                result = verify_telegram_authentication(bot_token=TELEGRAM_BOT_TOKEN, request_data=request.GET)

            except TelegramDataIsOutdatedError:
                return HttpResponse('Authentication was received more than a day ago.')

            except NotTelegramDataError:
                return HttpResponse('The data is not related to Telegram!')
            
            user_username = data.get('username')
            doc_data = get_staff_members()
            ic(doc_data.admins.values)
            ic(user_username)
            
            if user_username in doc_data.admins.values or user_username in doc_data.managers.values:
                # validation of manager ixist in db
                save_telegram_user(data)
                print('save complete')
                return redirect('main_panel')
            else:
                print(f'user {user_username} not in doc values')
        else:
            print('no hash')
            return redirect('login_page')

    return redirect('login_page')


def get_staff_members():
    sheet_id = "1dJl-3iTEpBWXJjkX183L0sx2FlQCVm4Ci0bc1iMGYhI"
    gid = "1496823880"
    excel = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx&gid={gid}"
    data = pd.read_excel(excel)
    data.columns = ['admins', 'managers','another']
    return data