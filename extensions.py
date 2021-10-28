import requests
import os
import json


class APIException (Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote_ticker, base_ticker):
        return requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')

    @staticmethod
    def convert(message):
        values = message.text.split(' ')
        answer = "NoErrors"
        if len(values) > 3:
            answer = f'Слишком много параметров'
            # raise APIException('Слишком много параметров')
        elif len(values) < 3:
            answer = f'Слишком мало параметров'
            # raise APIException('Слишком мало параметров')

        quote, base, amount = values

        if quote == base:
            answer = f'Невозможно конвертировать одинаковые валюты'
            # raise APIException(f'Невозможно конвертировать одинаковые валюты {base}.')

        try:
            quote_ticker = currencies_list[quote]
        except KeyError:
            answer = f'Недопустимая валюта {quote}'
            # raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = currencies_list[base]
        except KeyError:
            answer = f'Недопустимая валюта {quote}'
            # raise APIException(f'Не удалось обработать валюту {base}.')

        try:
            amount = amount
        except ValueError:
            answer = f'Недопустимая валюта {quote}'
            # raise APIException(f'Не удалось обработать количество {amount}.')

        rate = CryptoConverter.get_price(quote_ticker, base_ticker)
        return answer, quote, base, amount, rate


def open_currencies_file():  # Получение настроек бота
    if os.path.exists('currencies.json'):
        with open('currencies.json', 'r') as currencies_file:
            currencies_file = json.load(currencies_file)
    else:  # если файл настроек не найден
        empty_currencies = {'Euro': "EUR", 'Ruble': "RUB", 'Dollar': 'USD'}
        with open('currencies.json', 'w') as empty_currencies_file:
            # Создадим пустой файл настройки
            empty_currencies_file.write(json.dumps(empty_currencies))
            print("Нет файла настройки. Создан пустой файл настройки в текущем каталоге")
    return currencies_file


currencies_list = open_currencies_file()
