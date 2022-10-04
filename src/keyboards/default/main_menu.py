from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_kb = ReplyKeyboardMarkup([
    [
        KeyboardButton(text='ЗАГРУЗИТЬ ПЕСНЮ'),
    ],
    [
        KeyboardButton(text='МОИ ПЕСНИ'),
    ],
    [
        KeyboardButton(text='ДРУЗЬЯ'),
        KeyboardButton(text='ПОМОЩЬ')
    ]
],
    resize_keyboard=True
)