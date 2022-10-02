from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

view_chords_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('Посмотреть аккорды', callback_data='view_chords')
    ]
])
