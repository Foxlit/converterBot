import os
import json
import telebot

import extensions


def open_config_file():  # Получение настроек бота
    if os.path.exists('bot_config.json'):
        with open('bot_config.json', 'r') as config_file:
            bot_config_file = json.load(config_file)
    else:  # если файл настроек не найден
        insert_token = input("Введите токен бота: ")
        if len(insert_token) < 46:
            insert_token = "Please insert token here"
            print("Создан новый файл настройки в текущем каталоге, но бот не запущен. Укажите в файле 'bot_config.json'"
                  " корректный токен бота")
        else:
            print("Создан новый файл настройки в текущем каталоге с введенным токеном")
        empty_config = {'token': insert_token}
        with open('bot_config.json', 'w') as empty_config_file:
            # Создадим файл настройки
            empty_config_file.write(json.dumps(empty_config))
        if os.path.exists('bot_config.json'):
            with open('bot_config.json', 'r') as config_file:
                bot_config_file = json.load(config_file)
    return bot_config_file


bot_config = open_config_file()
bot = telebot.TeleBot(bot_config["token"])
currencies_list = extensions.get_currencies_list()


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу с ботом введите следующие данные:\nВалюта которую предстоит конвертировать\n' \
           'Валюта в которую предстоит конвертировать\nКоличество конвертируемой валюты\n' \
           'Например: доллар рубль 100\nКоманда /values - показывает доступные валюты\nКоманда /help - вызывает справку'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help_message(message: telebot.types.Message, available=None):
    text = 'Для конвертации введите следующие данные:\nВалюта из которой предстоит конвертировать\n' \
           'Валюта в которую предстоит конвертировать\nКоличество конвертируемой валюты\nНапример: доллар рубль 100'
    available_commands = '/help - справка\n'\
                         '/values - показать список досупных валют\n' \
                         '/add - добавить валюту'
    bot.send_message(message.chat.id, f'{text}\n {available_commands}')


@bot.message_handler(commands=['values', 'валюты'])
def currencies(message: telebot.types.Message):
    text = "Доступные валюты: "
    for currency in extensions.get_currencies_list():
        text = '\n'.join((text, currency,))
    bot.reply_to(message, text)


@bot.message_handler(commands=['add', 'добавить'])
def add(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Введите название валюты и через пробел буквенный код ответом на это сообщение")


@bot.message_handler(content_types=['text', ])
def convertattion(message: telebot.types.Message):
    replied_message = message.reply_to_message
    if replied_message is None:
        try:
            answer, quote, base, amount, total_base = extensions.CryptoConverter.convert(message)
            if answer == "":
                text = f'{amount} {quote} = {total_base} {base}'
                bot.send_message(message.chat.id, text)
            else:
                bot.send_message(message.chat.id, answer)
        except extensions.APIException as e:
            bot.send_message(message.chat.id, str(e))
    else:
        if replied_message.text == "Введите название валюты и через пробел буквенный код ответом на это сообщение":
            values = message.text.split(' ')
            if len(values) == 2:
                currency_name, currency_code = values
                extensions.open_currencies_file("add", currency_name.upper(), currency_code.upper())
                bot.reply_to(message, f"Валюта {currency_name.upper} ({currency_code.upper}) добавлена")
            else:
                bot.reply_to(message, "Ошибка ввода. Подвторите команду /add")


bot.polling()
