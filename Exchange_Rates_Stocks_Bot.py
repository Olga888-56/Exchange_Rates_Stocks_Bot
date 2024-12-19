import logging
import requests
import settings

from emoji import emojize
from glob import glob
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import choice, randint

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print("Вызван /start")
    context.user_data['emoji'] = get_smile(context.user_data)
    my_keyboard = ReplyKeyboardMarkup([
        ['/currency', '/Курсы криптовалют', '/Курсы акций'],
        ['/Справка']])
    print(f"Привет!{context.user_data['emoji']}")
    update.message.reply_text(
        f"Привет!{context.user_data['emoji']}", 
        reply_markup=my_keyboard)
    
def get_exchange_rates(api_key):
    url = f'https://data.fixer.io/api/latest?access_key={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"
    
api_key = '36141d9f61e2efc0816722f5663278d0'  
rates = get_exchange_rates(api_key)
print(rates)

def out_cur(update,context):
    context = get_exchange_rates(api_key)
    print(context)
    update.message.reply_text(rates)
   
#def currency():
#    GET https://data.fixer.io/api/latest

#    {
#        "base": USD,
#        "date": "2018-02-13",
#        "rates": {
#            "CAD": 1.260046,
#            "CHF": 0.933058,
#            "EUR": 0.806942,
#            "GBP": 0.719154,
#            [170 world currencies]
#        }
#    }

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, language = 'alias')
    return user_data['emoji']

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("currency", out_cur))
    dp.add_handler(MessageHandler(Filters.text, get_exchange_rates))
#    dp.add_handler(MessageHandler(Filters.regex('^(Курсы валют)$'), get_exchange_rates))
    
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()