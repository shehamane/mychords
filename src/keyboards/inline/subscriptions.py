from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.callback_datas import choose_friend_cd, get_friend_songs_cd


async def get_friends_kb(friends):
    return InlineKeyboardMarkup(inline_keyboard=([
                                                     [InlineKeyboardButton(friend.username,
                                                                           callback_data=choose_friend_cd.new(
                                                                               friend_id=friend.id))]
                                                     for friend in friends
                                                 ] + [[InlineKeyboardButton('Подписаться на пользователя',
                                                                            callback_data='new_friend')]]))


async def get_friend_info_kb(friend_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton('Песни пользователя', callback_data=get_friend_songs_cd.new(friend_id=friend_id))
        ]
    ])
