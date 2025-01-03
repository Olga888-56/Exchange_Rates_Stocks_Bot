from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

def anketa_start(update, context):
    update.message.reply_text(
        "Привет! Как Вас зовут?",
        reply_markup=ReplyKeyboardRemove()
    )
    print("Как вас зовут?")
    return "name"

def anketa_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text("Пожалуйста, введите имя и фамилию")
        return "name"
    else:
        context.user_data["anketa"] = {"name": user_name}
        reply_keyboard = [["EUR", "USD", "CNY", "GBP", "TRY"]]
        update.message.reply_text(
            "Выберите интересующую вас валюту",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
    #    print("что-то пошло не так")
        return "selected_currency"
    
def selected_currency(update,context):
    context.user_data["anketa"]["selected_currency"] = update.message.text
    print(context.user_data["anketa"]["selected_currency"])
    update.message.reply_text(f'Выбрана валюта {update.message.text}')