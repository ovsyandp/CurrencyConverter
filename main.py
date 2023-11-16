import telebot
from config import TOKEN
from extentions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}\
, это теллеграмм бот с помощью которого вы сможете конвертировать одну валюту в другую. Для того что бы узнать \
информацию как им пользоваться, введите комманду /help')

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, f'Для того что бы конвертировать валюту вам необходимо написать текст в \
формате:\n<имя валюты, цену которой вы хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество \
первой валюты>\nИнформацию о доступной для рассчета валюты вы можете узнать по комманде /values')

@bot.message_handler(commands=['values'])
def values_message(message):
    bot.send_message(message.chat.id, f'<b>рубль</b> — денежная единица Российской Федерации.\n<b>доллар</b> — денежная \
единица США.\n<b>евро</b> — официальная валюта 20 стран «еврозоны».', parse_mode='html')

@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Введите запрос в правильном формате\n<имя валюты, цену которой вы хотите \
узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>')
        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Ценна {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)