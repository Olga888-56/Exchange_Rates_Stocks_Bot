from glob import glob
from random import choice
from utils import get_smile, main_keyboard

def greet_user(update, context):
    print("Вызван /start")
    context.user_data['emoji'] = get_smile(context.user_data)
  
    print(f"Привет!{context.user_data['emoji']}")
    update.message.reply_text(
        f"Привет!{context.user_data['emoji']}", 
        reply_markup=main_keyboard())
    

def user_coordinates(update,context):
    coords = update.message.location
    print(coords)
    update.message.reply_text(f"Ваши координаты {coords}", reply_markup=main_keyboard())