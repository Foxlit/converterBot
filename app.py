import os
import json
import telebot
import requests
import extensions


class ConvertionException(Exception):
    print('Something wrong')

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


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу с ботом введите следующие данные:\n Валюта из которой предстоит конвертировать\n ' \
           'Валюта в которую предстоит конвертировать\n Количество конвертируемой валюты'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def currencies(message: telebot.types.Message):
    text = "Доступные валюты: "
    for currency in currencies_list:
        text = '\n'.join((text, currency,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convertattion(message: telebot.types.Message):
    quote, base, amount, rate = CryptoConverter.convert(message)
    total_base = json.loads(rate.content)[currencies_list[base]]
    quote_ticker = currencies_list[quote]
    base_ticker = currencies_list[base]
    text = f'Цена {amount} {quote} в {base} составляет: {total_base * int(amount)}'
    bot.send_message(message.chat.id, text)


class CryptoConverter:
    @staticmethod
    def convert(message):
        values = message.text.split(' ')

        if len(values) > 3:
            bot.send_message(message.chat.id, 'Слишком много параметров')
            raise ConvertionException('Слишком много параметров.')
        elif len(values) < 3:
            bot.send_message(message.chat.id, 'Слишком мало параметров')
            raise ConvertionException('Слишком мало параметров.')
        quote, base, amount = values

        if quote == base:
            # raise extensions.ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')
            # Не удалять, это пример
            bot.send_message(message.chat.id, 'Одинаковая валюта')
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = currencies_list[quote]
        except KeyError:
            bot.send_message(message.chat.id, 'Кривая валюта')
            raise ConvertionException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = currencies_list[base]
        except KeyError:
            bot.send_message(message.chat.id, 'Кривая валюта')
            raise ConvertionException(f'Не удалось обработать валюту {base}.')

        try:
            amount = float(amount)
        except ValueError:
            bot.send_message(message.chat.id, 'Кривое количество')
            raise ConvertionException(f'Не удалось обработать количество {amount}.')

        rate = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        return quote, base, amount, rate


bot.polling()

# api_key = bot_config["token"]
# bot.token['api_key'] = api_key
