from emoji import emojize
from random import choice, randint
import settings
from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, language = 'alias')
    return user_data['emoji']

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['/currency', '/Курсы криптовалют', '/Курсы акций'],
        ['/Справка'], [KeyboardButton('Мои координаты', request_location=True)]])