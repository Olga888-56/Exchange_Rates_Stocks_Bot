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
from jobs import send_cur_rate

logging.basicConfig(filename='bot.log', level=logging.INFO)


    
def get_exchange_rates(api_key):
    url = f'https://data.fixer.io/api/latest?access_key={api_key}&symbols=USD,EUR,GBP,JPY,CNY'
    response = requests.get(url)
#    data = json.load(response.text)

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return data["rates"], data["timestamp"]
        else:
            print("Ошибка в ответе API:",data.get("error",{}).get("info", "Неизвестная ошибка"))
    else:
        print("Ошибка при запросе к API:", response.status_code)
    return None, None
#        return response['rates'], ['RUB']
##        return response.json()
##    else:
##        return f"Error: {response.status_code}"


def save_to_csv(rates):
    if not rates:
        print("Нет данных для сохранения")
        return
           

    data_to_save = [
        ["Валюта", "Курс"],
        ["USD", rates["USD"]],
        ["EUR", rates["EUR"]],
        ["GPB", rates["GPB"]],
        ["JPY", rates["JPY"]],
        ["CNY", rates["CNY"]],
    ]

    with open('currency.csv', 'w', encoding='utf-8', newline='') as cur_csv:
        writer = csv.writer(cur_csv)
        writer.writerows(data_to_save)
    print("Данные успешно сохранены в currency.csv")

#def save_cur_rates_to_csv(rates, cur_csv):
#    with open(cur_csv, 'w', encoding='utf-8', newline='') as file:
#        writer = csv.writer(file)
#        writer.writerow(['Currency', 'Rate'])
#        for currency, rate in rates.items():
#            writer.writerow([currency, rate])
    


api_key = '36141d9f61e2efc0816722f5663278d0'  
rates = get_exchange_rates(api_key)


#if rates:
#    save_cur_rates_to_csv(rates, 'cur_csv')

with open('currency.json', 'w', encoding='utf-8', newline='') as cur_json:
#    data = json.load(cur_json)
#    print(data)
#with open('currency.json', 'r', encoding='utf-8') as cur_json:
#    rates = data['rates']
    fields = ['cur_name', 'rates']
    writer = csv.writer(cur_json)
    writer.writerow(['Currency', 'Rate'])
    print(type(rates))
    print(rates)
##    for currency, rate in rates.items():
#        print(type(row))
##        writer.writerow([currency, rate])
#        print(row)

#with open('currency.json', 'r') as cur_json:
#    data = json.load(cur_json)
#def get_selected_cur_rate(update: Update, context: CallbackContext):
#    selected_cur = context.user_data.get("anketa", {}).get("selected_currency")
#    rate = data['rates'].get(selected_cur)
#    if rate:
#        print(f"The exchange rate for {selected_cur} is: {rate}")
#    else:
#        print(f"Exchange rate for {selected_cur} not found.")

# Следующие строки закомментировала до января
with open('currency.json', 'r', encoding='utf-8') as cur_json:
    lines = cur_json.readlines()

##cur_rates_line = lines[5]
##cur_rates_dict = eval(cur_rates_line.split(",")[0].split(",")[0])
##print(cur_rates_dict)

##with open('currency.csv', 'w', newline='', encoding='utf-8') as cur_csv:
##    writer = csv.writer(cur_csv)
##    writer.writerow(['Currency', 'Rate'])
##    for currency, rate in cur_rates_dict.items():
##       writer.writerow([currency, rate])

print(rates)

def out_cur(update,context):
    context = get_exchange_rates(api_key)
    print(context)
    update.message.reply_text(rates)
   
def load_rates_from_csv(currency):
    rates = {}
    with open(currency, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            currency, rate = row
            print(currency)
#            rates[currency] = float(rate)
    print(rates)

##rates = load_rates_from_csv('currency.csv')


#user_currency = selected_currency.upper()

##if selected_currency in rates:
##    print(f"Курс {user_currency}: {rates[user_currency]}")
##else:
##    print("Курс по данной валюте не найден.")




def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    jq = mybot.job_queue
    jq.run_repeating(send_cur_rate, interval = 10)

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
    dp.add_handler(CommandHandler("currency", out_cur))
    dp.add_handler(MessageHandler(Filters.text, get_exchange_rates))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.regex('^(Курсы валют)$'), currencies_handler))
    
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()