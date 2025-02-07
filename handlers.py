from db import db, get_or_create_user
from glob import glob
from random import choice
from telegram.ext import RegexHandler
from utils import get_smile, main_keyboard

def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    print("Вызван /start")
    context.user_data['emoji'] = get_smile(context.user_data)
  
    print(f"Привет!{context.user_data['emoji']}")
    update.message.reply_text(
        f"Привет!{context.user_data['emoji']}", 
        reply_markup=main_keyboard())
    

def user_coordinates(update,context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    coords = update.message.location
    print(coords)
    update.message.reply_text(f"Ваши координаты {coords}", reply_markup=main_keyboard())


def currencies_handler(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CNY']
    update.message.reply_text("Выберите валюту:", reply_markup=ReplyKeyboardMarkup([currencies], resize_keyboard=True))
