# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from telegram import Bot
import asyncio
from register.models import TelegramUser
from django.http import JsonResponse
from icecream import ic
from django.contrib import messages
import requests as r

TOKEN = '7342161081:AAGWJEWpRTuukFyOO7xu_kkG_dbteBXayG8'
bot = Bot(token=TOKEN)

api_url = 'http://49.13.205.34:8060'
headers = {
    'access':'application/json',
    'Content-Type': 'application/json'
}


async def send_telegram_message(message):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id='-1002395487349', text=message)


def telegram_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            if request.session['is_authenticated'] == True:
                return view_func(request, *args, **kwargs)
            return redirect('login_page')
        except KeyError:
            return redirect('login_page')
    return _wrapped_view

# @telegram_login_required
def main_panel(request):
    if request.method == 'POST':
        ic(request.POST)
        contact_name = request.POST.get('contact_name')
        telephone_telegram = request.POST.get('telephone_telegram')
        description = request.POST.get('description')
        request_city = request.POST.get('request_city')
        city_out = request.POST.get('city_out')
        
        sum_of_request = request.POST.get('sum_of_request')
        currency_of_request = request.POST.get('currency_of_request')

        
        user_id = request.session['id']
        user = TelegramUser.objects.get(id=user_id)

        message = f'''
Вiд: @{user.username}

Місто звернення/заносу: {request_city}
Місто видачi: {city_out}
Ім'я клієнта: {contact_name}
Телефон/Телеграм: {telephone_telegram}
Опис запиту: {description}
Сума: {sum_of_request} {currency_of_request}
'''
        data = {
            'from_manager':user.username,
            'request_city':request_city,
            'issuing_city':city_out,
            'client_name':contact_name,
            'client_phone':telephone_telegram,
            'request_description':description,
            'request_sum':f'{sum_of_request} {currency_of_request}'
        }
        result = asyncio.run(send_telegram_message(message))
        res = r.post(f"{api_url}/call_request", headers=headers, json=data)
        if res.status_code == 200:
            messages.info(request, 'Okay')
        else:
            messages.error(request, str(res.status_code))

        messages.info(request, str(result))
        # -1002395487349
        return redirect('main_panel')  # Redirect to a success page
    elif request.method == 'GET':
        user_id = request.session['id']
        user = TelegramUser.objects.get(id=user_id)

        profile_data = {
            'first_name': user.first_name,
            'username':user.username,  # Assuming you have this field
            'profile_picture': user.photo_url,  # Assuming you have this field
        }
        currencies = scrape_google_sheets_currency()
        cities = ["Рівне","Вінниця",
            "Кропивницький","Черкаси","Дніпро","Тернопіль","Хмельницький",
            "Кривий Ріг","Ужгород","Київ","Запоріжжя","Миколаїв","Суми",
            "Чернігів","Чернівці","Івано-Франківськ","Житомир",
            "Луцьк","Харків", "Кременчук", "Полтава", "Мукачево",]
        # Step 4: Return the profile data as a JSON response
        # return JsonResponse(profile_data, status=200)
        print('someone just got access to page')
        return render(request, 'request_form.html',
                        {'title':'Створення заявки',
                        'profile_photo':profile_data['profile_picture'],
                        'first_name':profile_data['first_name'],
                        'username':profile_data['username'],
                        'cities':cities,
                        'currencies':currencies})
        

def logout(request):
    request.session['is_authenticated'] = False
    return redirect('login_page')

import requests
from bs4 import BeautifulSoup

url_cods = 'https://docs.google.com/spreadsheets/d/1dJl-3iTEpBWXJjkX183L0sx2FlQCVm4Ci0bc1iMGYhI/edit?gid=617465825#gid=617465825'
def scrape_google_sheets_currency(url: str = url_cods):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        if table:
            data = []
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if cells:
                    data.append([cell.text.strip() for cell in cells])
            currency_dict = {row[0]: row[1] for row in data[1:]}  # Create a dictionary from the data
            del currency_dict['']
            
            currencies = {}

            for key, value in currency_dict.items():
                currencies[key] = float(value.replace(',', '.'))

            # ic(currency_dict)
            return currencies
        else:
            return "Failed to retrieve data. Check the URL and try again."
    else:
        return "Failed to retrieve data. Check the URL and try again."
