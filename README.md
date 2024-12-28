# Проект Exchange_Rates_Stocks_Bot

Exchange_Rates_Stocks_Bot - это бот для телеграм, который прислыает пользователю курсы валют, криптовалют и акций.

## Установка

1. Клонируйте репозиторий с github
2. Создайте виртуальное окружение 
3. Установите зависимости `pip install -r requirements.txt`
4. Создайте файл `settings.py`
5. Впишите в settings.py переменные:
```
API_KEY = "API-ключ бота"
USER_EMOJI = ['::one::', '::two::', '::three::', '::four::', '::five::']
```
6. Запустите бота командой `python Exchange_Rates_Stocks_Bot.py`