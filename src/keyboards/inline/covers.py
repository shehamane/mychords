from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.callback_datas import choose_cover_cd, send_cover_cd, delete_cover_cd


async def get_covers_kb(covers):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(cover.name, callback_data=choose_cover_cd.new(cover_id=cover.id))]
        for cover in covers
    ])


async def get_cover_info_kb(cover_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Послушать',
                                 callback_data=send_cover_cd.new(cover_id=cover_id)),
            InlineKeyboardButton(text='Удалить',
                                 callback_data=delete_cover_cd.new(cover_id=cover_id)),
        ],
    ])
