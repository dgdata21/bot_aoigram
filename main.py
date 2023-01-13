import secrets
import string

from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import text
from aiogram.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from config import bot
from kb import *
# from fms import *
# from fms import pass_level
# from fms import Pswd
# from fms import length

bot = bot
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

global pass_level
global length


class Pswd(StatesGroup):
    pass_level = State()
    pass_len = State()

@dp.message_handler(commands='start')
async def get_start(message: types.Message):
    await message.answer('👋 Привет!',
                         reply_markup=markup)
    await message.answer('Я бот-генератор паролей!', reply_markup=markup1)


help_msg = text('/start - Перезапуск бота\n'
                '/start_generation - начало работы\n'
                '/pwd - генерация пароля')

@dp.message_handler(commands='help')
async def help_cmd(message: types.Message):
    await message.answer(help_msg)


@dp.message_handler(lambda message: message.text == "Меню комманд")
async def registration(message: types.Message):
    await message.answer(help_msg)


@dp.message_handler(commands='start_generation')
async def get_name(message: types.Message):
    await Pswd.pass_level.set()
    await message.answer('Выбери уровень сложности пароля:\n'
                         '1 - light\n'
                         '2 - medium\n'
                         '3 - hard\n'
                         '4 - token hex')


@dp.message_handler(lambda message: not message.text.isdigit(), state=Pswd.pass_level)
async def process_level_invalid(message: types.Message):
    return await message.answer('Можно только цифры')


@dp.message_handler(lambda message: int(message.text) > 4, state=Pswd.pass_level)
async def process_level_range(message: types.Message):
    return await message.answer('Out of range')


@dp.message_handler(state=Pswd.pass_level)
async def process_level(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pass_level'] = message.text
        global pass_level
        pass_level = int(data['pass_level'])
    await Pswd.next()
    await message.answer('Выбери длину пароля')


@dp.message_handler(lambda message: not message.text.isdigit(), state=Pswd.pass_len)
async def process_len_invalid(message: types.Message):
    return await message.answer('Можно только цифры')


@dp.message_handler(lambda message: message.text.isdigit(), state=Pswd.pass_len)
async def process_len(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pass_len'] = message.text
    global length
    length = int(data['pass_len'])
    await message.answer('Для получения пароля введи команду /pwd\n'
                         'Для повторной генерации введи команду /start_generation')
    await state.finish()


@dp.message_handler(commands='pwd')
async def pass_gen(message: types.Message):
    if pass_level == 4:
        pass_new = secrets.token_hex()
        await message.answer('token готов:\n' + pass_new)
    elif pass_level == 3:
        passwd = string.ascii_letters + string.digits + string.punctuation
        pass_new = ''.join(secrets.choice(passwd) for i in range(length))
        await message.answer('Пароль готов:\n' + pass_new)
    elif pass_level == 2:
        passwd = string.ascii_letters + string.digits
        pass_new = ''.join(secrets.choice(passwd) for i in range(length))
        await message.answer('Пароль готов:\n' + pass_new)
    elif pass_level == 1:
        passwd = string.ascii_letters
        pass_new = ''.join(secrets.choice(passwd) for i in range(length))
        await message.answer('Пароль готов:\n' + pass_new)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
