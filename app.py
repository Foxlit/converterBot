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


bot_config = open_config_file()
bot = telebot.TeleBot(bot_config["token"])
h=7

@bot.message_handler()
def echo_test(messege: telebot.types.Message):
    bot.send_message(messege.chat.id, "hello")


bot.polling()

# api_key = bot_config["token"]
# bot.token['api_key'] = api_key
