from django_telegram_login.errors import (
    NotTelegramDataError,TelegramDataIsOutdatedError,)
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, HttpResponse, redirect
from .models import TelegramUser 
import json
from icecream import ic
import pandas as pd
from django.contrib.auth import login
from django_telegram_login.authentication import verify_telegram_authentication
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
    auth_date = data.get('auth_date')

    # Create or update the user
    user, created = TelegramUser.objects.update_or_create(
        id=user_id,
        defaults={
            'first_name': first_name,
            'username': username,
            'photo_url': photo_url,
            'auth_date': auth_date})
    
    print('user_created')
    return user, created  # Returns the user instance and a boolean indicating if it was created

def login_authentication(request):
    if request.method == "GET":
        if 'is_authenticated' in request.session:
            if request.session['is_authenticated'] == True:
                print('user is authenticated')
                return redirect('main_panel')
        else:
            print(request)
            print(request.user)
            print('--')

        if request.GET.get('hash'):
            ic('hash was found')
            data = request.GET
            ic(data)
            try:
                result = verify_telegram_authentication(bot_token=TELEGRAM_BOT_TOKEN, request_data=request.GET)
                print(result)
                user_username = data.get('username')
                doc_data = get_staff_members()
                ic(doc_data.admins.values)
                ic(user_username)
                
                if any(user_username in array for array in (doc_data.managers.values, doc_data.admins.values, doc_data.another.values)):
                    # validation of manager ixist in db
                    print('user in doc_data admins or managerss or another')
                    save_telegram_user(data)
                    request.session['is_authenticated'] = True
                    request.session['id'] = data.get('id')

                else:
                    print(f'user {user_username} not in doc values')

                return redirect('main_panel')

            except TelegramDataIsOutdatedError:
                return HttpResponse('Authentication was received more than a day ago.')

            except NotTelegramDataError:
                return HttpResponse('The data is not related to Telegram!')
            
            
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