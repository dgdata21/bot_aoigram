from aiogram.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


button1 = KeyboardButton(text='Меню комманд', callback_data='/help')
button2 = InlineKeyboardButton(text='Полезные ссылки',
                               url='http://it-uroki.ru/uroki/bezopasnost/parol/'
                                   'pravila-sozdaniya-i-xraneniya-parolej.html')
button3 = InlineKeyboardButton(text='Полезные ссылки',
                               url='https://habr.com/ru/company/dataline/blog/563228/')
markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.row(button1)
markup1 = InlineKeyboardMarkup()
markup1.row(button2, button3)