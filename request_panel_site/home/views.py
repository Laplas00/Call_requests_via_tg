# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from telegram import Bot
import asyncio

TOKEN = '7342161081:AAGWJEWpRTuukFyOO7xu_kkG_dbteBXayG8'
bot = Bot(token=TOKEN)

async def send_telegram_message(message):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id='-1002395487349', text=message)


# @login_required
def main_panel(request):
    if request.method == 'POST':
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
        if len(request.GET) > 1:
            print('more than one parametr in this query')
            return render(request, 'request_form.html',{'title':'Main page'})
        else:
            print('someone just got access to page')
            return render(request, 'request_form.html',{'title':'Main page'})
