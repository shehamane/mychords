from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.callback_datas import choose_song_cd, view_chords_cd, delete_song_cd, new_cover_cd, send_song_cd, \
    get_covers_cd


async def get_songs_list_kb(page_list, page, total):
    kb = InlineKeyboardMarkup()

    for song in page_list:
        kb.inline_keyboard.append(
            [
                InlineKeyboardButton(text=f'{song.name} - {song.author}, {song.duration}',
                                     callback_data=choose_song_cd.new(song_id=song.id)),
            ]
        )
    kb.inline_keyboard.append(
        [
            InlineKeyboardButton(text='<=', callback_data='previous'),
            InlineKeyboardButton(text=f'{page}/{total}', callback_data='page'),
            InlineKeyboardButton(text='=>', callback_data='next'),
        ]
    )

    return kb


async def get_song_info_kb(song_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Посмотреть аккорды',
                                 callback_data=view_chords_cd.new(song_id=song_id)),
        ],
        [
            InlineKeyboardButton(text='Послушать',
                                 callback_data=send_song_cd.new(song_id=song_id)),
            InlineKeyboardButton(text='Удалить',
                                 callback_data=delete_song_cd.new(song_id=song_id)),
        ],
        [
            InlineKeyboardButton(text='Записать кавер',
                                 callback_data=new_cover_cd.new(song_id=song_id)),
            InlineKeyboardButton(text='Мои каверы',
                                 callback_data=get_covers_cd.new(song_id=song_id)),
        ],
    ])
