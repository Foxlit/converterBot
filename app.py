import os
import json
import telebot

import extensions


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


bot_config = open_config_file()
bot = telebot.TeleBot(bot_config["token"])
currencies_list = extensions.open_currencies_file()


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу с ботом введите следующие данные:\n Валюта из которой предстоит конвертировать\n ' \
           'Валюта в которую предстоит конвертировать\n Количество конвертируемой валюты'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help_message(message: telebot.types.Message, available=None):
    text = 'Для конвертации введите следующие данные:\n Валюта из которой предстоит конвертировать\n ' \
           'Валюта в которую предстоит конвертировать\n Количество конвертируемой валюты'
    available_commands = '/help - справка\n'\
                         '/values - показывает список досупных валют'
    bot.send_message(message.chat.id, f'{text}\n {available_commands}')


@bot.message_handler(commands=['values'])
def currencies(message: telebot.types.Message):
    text = "Доступные валюты: "
    for currency in currencies_list:
        text = '\n'.join((text, currency,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convertattion(message: telebot.types.Message):
    try:
        answer, quote, base, amount, rate = extensions.CryptoConverter.convert(message)
        if answer == "":
            total_base = json.loads(rate.content)[currencies_list[base]]
            text = f'{amount} {quote} = {total_base * amount} {base}'
            bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, answer)
    except extensions.APIException as e:
        bot.send_message(message.chat.id, str(e))


bot.polling()
