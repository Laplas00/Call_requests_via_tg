# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from telegram import Bot
import asyncio
from register.models import TelegramUser
from django.http import JsonResponse
from icecream import ic

TOKEN = '7342161081:AAGWJEWpRTuukFyOO7xu_kkG_dbteBXayG8'
bot = Bot(token=TOKEN)

async def send_telegram_message(message):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id='-1002395487349', text=message)


def telegram_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            if request.session['is_authenticated'] == True:
                return view_func(request, *args, **kwargs)
            return redirect('login page')
        except KeyError:
            return redirect('login page')
    return _wrapped_view

@telegram_login_required
def main_panel(request):
    if request.method == 'POST':
        ic(request.POST)
        contact_data = request.POST.get('contact_data')
        description = request.POST.get('description')
        sum_of_request = request.POST.get('sum_of_request')
        currency_of_request = request.POST.get('currency_of_request')
        print(contact_data)
        print(description)
        print(sum_of_request)
        print(currency_of_request)
        message = f'''
Контакт: {contact_data}
Описание: {description}
Сумма запроса: {sum_of_request}
Валюта: {currency_of_request}
'''
        asyncio.run(send_telegram_message(message))
        # -1002395487349
        return redirect('main_panel')  # Redirect to a success page
    elif request.method == 'GET':
        user_id = request.session['id']
        user = TelegramUser.objects.get(id=user_id)

        profile_data = {
            'first_name': user.first_name,  # Assuming you have this field
            'profile_picture': user.photo_url,  # Assuming you have this field
        }
        
        # Step 4: Return the profile data as a JSON response
        # return JsonResponse(profile_data, status=200)
        print('someone just got access to page')
        return render(request, 'request_form.html',
                        {'title':'Main page',
                        'profile_photo':profile_data['profile_picture'],
                        'first_name':profile_data['first_name'] })
        

def logout(request):
    request.session['is_authenticated'] = False
    return redirect('login')