import requests
import os
import json


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote, base, amount=1):
        req = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={get_currencies_list()[quote]}'
                           f'&tsyms={get_currencies_list()[base]}')
        rate = json.loads(req.content)[get_currencies_list()[base]]
        return rate * amount

    @staticmethod
    def convert(message):
        values = message.text.split(' ')
        quote = base = amount = answer = ""
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
                curr_list = get_currencies_list()
                try:
                    quote_ticker = curr_list[quote]
                except KeyError:
                    answer += f'Недопустимая валюта "{quote}"\n чтобы узнать список допустимых валют введите /values'

                # Проверим, входит ли вторая валюта в список валют
                try:
                    base_ticker = curr_list[base]
                except KeyError:
                    answer += f'Недопустимая валюта "{base}"\n чтобы узнать список допустимых валют введите /values'
        except ValueError:
            if len(values) > 3:
                answer += f'Слишком много параметров'
            elif len(values) < 3:
                answer += f'Слишком мало параметров'

        if answer != "":
            raise APIException(answer)
        total_base = CryptoConverter.get_price(quote, base, amount)
        return answer, quote, base, amount, total_base


def open_currencies_file(mode="read", added_name=None, added_code=None):  # Получение валют бота
    if mode == "read":
        if os.path.exists('currencies.json'):
            with open('currencies.json', 'r', encoding='utf-8') as currencies_file:
                currencies_file = json.load(currencies_file)
        else:  # если файл валют не найден
            empty_currencies = {'ЕВРО': "EUR", 'РУБЛЬ': "RUB", 'ДОЛЛАР': 'USD'}
            with open('currencies.json', 'w') as empty_currencies_file:
                # Создадим файл валют
                empty_currencies_file.write(json.dumps(empty_currencies, indent=4))
                print("Нет файла валют. Создан новый файл валют в текущем каталоге")
            with open('currencies.json', 'r', encoding='utf-8') as currencies_file:
                currencies_file = json.load(currencies_file)
        return currencies_file
    elif mode == "add":
        if os.path.exists('currencies.json'):
            with open('currencies.json', 'r', encoding='utf-8') as currencies_file:
                currencies = json.load(currencies_file)
            f = open('currencies.json', 'w')
            f.close()
            with open('currencies.json', 'w', encoding='utf-8') as currencies_file:
                print(currencies_file)
                added_currency = {added_name: added_code}
                print(added_currency)
                currencies.update(added_currency)
                print(currencies_file)
                currencies_file.write(json.dumps(currencies, indent=4))


def get_currencies_list():
    return open_currencies_file("read")


currencies_list = get_currencies_list()
