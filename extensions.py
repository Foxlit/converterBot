import requests
import os
import json


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote_ticker, base_ticker):
        return requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')

    @staticmethod
    def convert(message):
        values = message.text.split(' ')
        quote_ticker = base_ticker = quote = base = amount = answer = ""
        try:
            quote, base, amount = values
            quote = quote.upper()

            base = base.upper()
            try:
                amount = float(amount)
            except Exception:
                answer += f'Некорректный ввод, введите число\n'

            if quote == base:
                answer += f'Невозможно конвертировать одинаковые валюты: "{base}"'
            else:
                # Проверим, входит ли первая валюта в список валют
                try:
                    quote_ticker = currencies_list[quote]
                except KeyError:
                    answer += f'Недопустимая валюта "{quote}"\n чтобы узнать список допустимых валют введите /values'

                # Проверим, входит ли вторая валюта в список валют
                try:
                    base_ticker = currencies_list[base]
                except KeyError:
                    answer += f'Недопустимая валюта "{base}"\n чтобы узнать список допустимых валют введите /values'
        except ValueError:
            if len(values) > 3:
                answer += f'Слишком много параметров'
            elif len(values) < 3:
                answer += f'Слишком мало параметров'

        if answer != "":
            raise APIException(answer)
        rate = CryptoConverter.get_price(quote_ticker, base_ticker)
        return answer, quote, base, amount, rate


def open_currencies_file():  # Получение валют бота
    if os.path.exists('currencies.json'):
        with open('currencies.json', 'r', encoding='utf-8') as currencies_file:
            currencies_file = json.load(currencies_file)
    else:  # если файл валют не найден
        empty_currencies = {'ЕВРО': "EUR", 'РУБЛЬ': "RUB", 'ДОЛЛАР': 'USD'}
        with open('currencies.json', 'w') as empty_currencies_file:
            # Создадим файл валют
            empty_currencies_file.write(json.dumps(empty_currencies, indent=4))
            print("Нет файла валют. Создан пустой файл валют в текущем каталоге")
        with open('currencies.json', 'r', encoding='utf-8') as currencies_file:
            currencies_file = json.load(currencies_file)
    return currencies_file


currencies_list = open_currencies_file()
