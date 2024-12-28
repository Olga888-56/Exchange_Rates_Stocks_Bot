import csv
import json
import logging
import requests
import settings


from glob import glob
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext)
from telegram import Update
from anketa import anketa_start, anketa_name, selected_currency
from handlers import greet_user, user_coordinates

logging.basicConfig(filename='bot.log', level=logging.INFO)


    
def get_exchange_rates(api_key):
    url = f'https://data.fixer.io/api/latest?access_key={api_key}'
    response = requests.get(url)
#    data = json.load(response.text)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"


api_key = '36141d9f61e2efc0816722f5663278d0'  
rates = get_exchange_rates(api_key)

with open('currency.json', 'w', encoding='utf-8', newline='') as cur_json:
#    data = json.load(cur)
#    print(data)
    fields = ['cur_name', 'rates']
    writer = csv.writer(cur_json)
    writer.writerow(['Currency', 'Rate'])
    print(type(rates))
    for currency, rate in rates.items():
#        print(type(row))
        writer.writerow([currency, rate])
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
#with open('currency.json', 'r', encoding='utf-8') as cur_json:
#    lines = cur_json.readlines()

#cur_rates_line = lines[2]
#cur_rates_dict = eval(cur_rates_line)
#print(cur_rates_dict)

#with open('currency.csv', 'w', newline='', encoding='utf-8') as cur_csv:
#    writer = csv.writer(cur_csv)
#    writer.writerow(['Currency', 'Rate'])
#    for currency, rate in cur_rates_dict.items():
#        writer.writerow([currency, rate])

print(rates)

def out_cur(update,context):
    context = get_exchange_rates(api_key)
    print(context)
    update.message.reply_text(rates)
   






def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
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
#    dp.add_handler(MessageHandler(Filters.regex('^(Курсы валют)$'), get_exchange_rates))
    
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()