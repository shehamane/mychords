from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(Text(contains=['помощь'], ignore_case=True), state='*')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Регистрация',
        '/help - Получить справку',
        '/menu - Открыть меню',
        'Для отмены любого действия пишите "отмена"',
        'Чтобы показать меню необходимо нажать на кнопку рядом с полем ввода сообщений',
    ]
    await message.answer('\n'.join(text))
