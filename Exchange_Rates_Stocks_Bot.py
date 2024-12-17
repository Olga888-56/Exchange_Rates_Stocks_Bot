from telegram.ext import Updater, CommandHandler

import settings

def greet_user(update, context):
    print("Вызван /start")
    update.message.reply_text("Привет!")

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    
    mybot.start_polling()
    mybot.idle()

main()