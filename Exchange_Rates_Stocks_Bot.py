import csv
import json
import logging
import requests
import settings


from glob import glob
from datetime import datetime
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler,CallbackContext)
from telegram import Update
from anketa import anketa_start, anketa_name, selected_currency
from handlers import greet_user, user_coordinates, currencies_handler
from save_to_csv import save_to_csv
##from jobs import send_cur_rate

logging.basicConfig(filename='bot.log', level=logging.INFO)

def get_exchange_rates_updater(context):
    get_exchange_rates()
    
def get_exchange_rates(api_key = ""):
    if api_key == "":
        api_key = settings.Exchanger_API_KEY
        print(api_key)
    url = f'https://data.fixer.io/api/latest?access_key={api_key}&symbols=USD,EUR,GBP,JPY,CNY'
    response = requests.get(url)
   


    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return data["rates"], data["timestamp"]
        else:
            print("Ошибка в ответе API:",data.get("error",{}).get("info", "Неизвестная ошибка"))
    else:
        print("Ошибка при запросе к API:", response.status_code)
    return None, None


with open('currency.json', 'w', encoding='utf-8', newline='') as cur_json:
    fields = ['cur_name', 'rates']
    writer = csv.writer(cur_json)
    writer.writerow(['Currency', 'Rate'])

with open('currency.json', 'r', encoding='utf-8') as cur_json:
    lines = cur_json.readlines()

def currencies_update(update,context):
    api_key = settings.Exchanger_API_KEY
    rates = get_exchange_rates(api_key)
###    context.user_data["rates"] = rates
    print(rates)
    update.message.reply_text(rates)
   
def load_rates_from_csv(currency):
    rates = {}
    with open(currency, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            currency, rate = row
            print(currency)
    print(rates)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    jq = mybot.job_queue
    jq.run_repeating(get_exchange_rates_updater, interval = 600)

    dp = mybot.dispatcher

   
    anketa = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Заполнить анкету)$'), anketa_start)
        ],
        states={
            "name": [MessageHandler(Filters.text, anketa_name)],
            "selected_currency": [MessageHandler(Filters.regex('^(EUR|USD|CNY|GBP|TRY)$'), selected_currency)]
        },
        fallbacks=[]
    )
    
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("currency", currencies_update))
    dp.add_handler(CommandHandler("update_rates", get_exchange_rates))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.regex('^(Курсы валют)$'), currencies_handler))
    
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()