from pymongo import MongoClient
#from anketa import selected_currency
import settings

client = MongoClient(
    settings.MONGO_LINK
)

db = client[settings.MONGO_DB]

def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({"user_id": effective_user.id})
    print(effective_user.__dict__)
    if not user:
        user = {
            "user_id": effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "username": effective_user.username,
            "selected_currency": context.user_data["selected_currency"],
            "chat_id": chat_id
        }
        db.users.insert_one(user)
        print(f'selected_currency {selected_currency}')
    return user

def update_user_currency(db, effective_user, selected_currency):
    try:
        effective_user['currency'] = selected_currency
        db.users.update_one(
            {"user_id": effective_user.id},
            {"$set": {"currency": selected_currency}}
        )
        print(f"Валюта пользователя {effective_user.get("username")} успешно обновлена на {selected_currency}")
    except Exception as e:
        print(f"Ошибка при обновлении валюты: {e}")



