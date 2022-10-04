import telebot

from config import TOKEN, keys
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(massage: telebot.types.Message):
    text = 'Для начала работы введите команду для бота в следующем формате:\n <имя вылюты которую нужно конвертировать> \
\n <имя валюты в которую нужно конверитировать>\
\n <количество первой валюты> \n <Увидеть список доступных валют: /values>'
    bot.reply_to(massage, text)


@bot.message_handler(commands=['values'])
def value(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {round(total_base*float(amount), 2)}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
