from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_chords_kb(page_num, page_total):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='<=', callback_data='previous'),
            InlineKeyboardButton(text=f'{page_num}/{page_total}', callback_data='page'),
            InlineKeyboardButton(text='=>', callback_data='next'),
        ]
    ])
