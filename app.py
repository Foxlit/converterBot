import os
import json
import telebot


def open_config_file():  # Получение настроек бота
    if os.path.exists('bot_config.json'):
        with open('bot_config.json', 'r') as config_file:
            bot_config_file = json.load(config_file)
    else:  # если файл настроек не найден
        empty_config = {'token': 0}
        with open('bot_config.json', 'w') as empty_config_file:
            # Создадим пустой файл настройки
            empty_config_file.write(json.dumps(empty_config))
            print("Нет файла настройки. Создан пустой файл настройки в текущем каталоге")
    return bot_config_file


def open_currencies_file():  # Получение настроек бота
    if os.path.exists('currencies.json'):
        with open('currencies.json', 'r') as currencies_file:
            currencies_file = json.load(currencies_file)
    else:  # если файл настроек не найден
        empty_currencies = {'Bitcoin': "BTC", 'Ruble': "RUB", 'Dollar': 'USD'}
        with open('currencies.json', 'w') as empty_currencies_file:
            # Создадим пустой файл настройки
            empty_currencies_file.write(json.dumps(empty_currencies))
            print("Нет файла настройки. Создан пустой файл настройки в текущем каталоге")
    return currencies_file


currencies_list = open_currencies_file()
bot_config = open_config_file()
bot = telebot.TeleBot(bot_config["token"])


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу с ботом введите следующие данные:\n Валюта из которой предстоит конвертировать\n ' \
        'Валюта в которую предстоит конвертировать\n Количество конвертируемой валюты'
    bot.reply_to(message, text)


@bot.message_handler(commands=['currencies'])
def currencies(message: telebot.types.Message):
    text = "Доступные валюты: "
    for currency in currencies_list:
        text = '\n'.join((text, currency, ))
    bot.reply_to(message, text)


bot.polling()

# api_key = bot_config["token"]
# bot.token['api_key'] = api_key
