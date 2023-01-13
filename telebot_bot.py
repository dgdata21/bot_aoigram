import telebot
import string
import secrets
from telebot import types

bot = telebot.TeleBot('5713546444:AAHSLg8ZoFCd4-xZhiuc8rU4CbUenwMoh2g')
length = 0


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню команд')
    btn2 = types.KeyboardButton('Полезные ссылки')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, '👋 Привет! Я бот-генератор паролей!\n'
                                           'Полный список команд - кнопка "Меню команд"', reply_markup=markup)


@bot.message_handler(commands=['input'])
def len_query(message):
    bot.send_message(message.from_user.id, 'Введите требуемую длину пароля:\n')
    bot.register_next_step_handler(message, pass_len)


def pass_len(message):
    global length
    length = int(message.text)
    return length


@bot.message_handler(commands=['passwd_letters'])
def pass_gen(message):
    passwd = string.ascii_letters
    pass_new = ''.join(secrets.choice(passwd) for i in range(length))
    bot.send_message(message.from_user.id, 'Ваш пароль:\n' + pass_new)


@bot.message_handler(commands=['passwd_digits'])
def pass_gen(message):
    passwd = string.digits
    pass_new = ''.join(secrets.choice(passwd) for i in range(length))
    bot.send_message(message.from_user.id, 'Ваш пароль:\n' + pass_new)


@bot.message_handler(commands=['passwd_letters_digits'])
def pass_gen(message):
    passwd = string.ascii_letters + string.digits
    pass_new = ''.join(secrets.choice(passwd) for i in range(length))
    bot.send_message(message.from_user.id, 'Ваш пароль:\n' + pass_new)


@bot.message_handler(commands=['passwd_special_symbols'])
def pass_gen(message):
    passwd = string.ascii_letters + string.digits + string.punctuation
    pass_new = ''.join(secrets.choice(passwd) for i in range(length))
    bot.send_message(message.from_user.id, 'Ваш пароль:\n' + pass_new)


@bot.message_handler(commands=['token_hex'])
def pass_gen(message):
    pass_new = secrets.token_hex(length)
    bot.send_message(message.from_user.id, 'Ваш token:\n' + pass_new)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Меню команд':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.from_user.id, 'Меню команд\n'
                                               '/input - length of password\n'
                                               '/passwd_letters - generate password with letters only\n'
                                               '/passwd_digits - generate password with digits only\n'
                                               '/passwd_letters_digits - generate password with letters and digits\n'
                                               '/passwd_special_symbols - generate password with special symbols\n'
                                               '/token_hex - generate hex-token\n'
                                               '', reply_markup=markup)
    elif message.text == 'Полезные ссылки':
        bot.send_message(message.from_user.id,
                         'http://it-uroki.ru/uroki/bezopasnost/parol/pravila-sozdaniya-i-xraneniya-parolej.html\n')
        bot.send_message(message.from_user.id,
                         'https://habr.com/ru/company/dataline/blog/563228/')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
