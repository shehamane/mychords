from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message

from filters.username import IsUsernameFilter
from keyboards.inline.songs import get_songs_list_kb
from keyboards.inline.subscriptions import get_friends_kb, get_friend_info_kb
from states.subscriptions import Subscriptions

from loader import dp
from utils.callback_datas import choose_friend_cd, get_friend_songs_cd
from utils.db_api.api import db_api as db


@dp.message_handler(Text(contains=['друзья'], ignore_case=True), state='*')
async def get_subscriptions_list(message: Message, state: FSMContext):
    await state.finish()
    user = await db.get_current_user()
    subscriptions = await db.get_user_subscriptions(user.id)
    async with state.proxy() as data:
        data['pinned_msg'] = await message.answer('Список подписок:',
                                                  reply_markup=await get_friends_kb(subscriptions))
    await Subscriptions.SubscriptionsList.set()


@dp.callback_query_handler(text='new_friend', state=Subscriptions.all_states)
async def request_username(call: CallbackQuery):
    await call.message.answer('Введите юзернейм пользователя...')
    await Subscriptions.SubscriptionAddition.set()


@dp.message_handler(IsUsernameFilter(), state=Subscriptions.SubscriptionAddition)
async def add_subscription(message: Message, state: FSMContext):
    user = await db.get_current_user()
    subscribed = await db.get_user_by_username(message.text[1:])
    if subscribed:
        await db.create_subscription(subscribed.id, user.id)
        subscriptions = await db.get_user_subscriptions(user.id)
        async with state.proxy() as data:
            await data['pinned_msg'].edit_text('Вы подписались на пользователя',
                                               reply_markup=await get_friends_kb(subscriptions))
        await Subscriptions.SubscriptionsList.set()
    else:
        subscriptions = await db.get_user_subscriptions(user.id)
        async with state.proxy() as data:
            await data['pinned_msg'].edit_text('Пользователь не найден',
                                               reply_markup=await get_friends_kb(subscriptions))
        await Subscriptions.SubscriptionsList.set()


@dp.callback_query_handler(choose_friend_cd.filter(), state=Subscriptions.SubscriptionsList)
async def get_friend_info(call: CallbackQuery, callback_data: dict):
    friend_id = int(callback_data['friend_id'])
    friend = await db.get_user(friend_id)
    await call.message.answer(text=f'Пользователь {friend.username}',
                              reply_markup=await get_friend_info_kb(friend_id))
    await Subscriptions.SubscriptionsInfo.set()


@dp.callback_query_handler(get_friend_songs_cd.filter(), state=Subscriptions.SubscriptionsSong)
async def get_friends_songs(call: CallbackQuery, callback_data: dict, state: FSMContext):
    friend_id = int(callback_data['friend_id'])
    friend = await db.get_user(friend_id)


    async with state.proxy() as data:
        data['friend_id'] = friend_id
        data['page_num'] = 0
        data['page_total'] = await db.count_user_songs_list_pages(friend.id) + 1

        kb = await get_songs_list_kb(await db.get_user_songs_list(friend.id, 0), 1, data['page_total'])
        await call.message.answer(f'Песни пользователя {friend.username}:', reply_markup=kb)
    await Subscriptions.SubscriptionsSong.set()


@dp.callback_query_handler(text='next', state=Subscriptions.SubscriptionsSong)
async def show_next_page(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data['page_num'] < await db.count_user_songs_list_pages(data['friend_id']):
            data['page_num'] += 1
            kb = await get_songs_list_kb(await db.get_user_songs_list(data['friend_id'], data['page_num']),
                                         data['page_num'] + 1, data['page_total'])
            await call.message.edit_reply_markup(kb)


@dp.callback_query_handler(text='previous', state=Subscriptions.SubscriptionsSong)
async def show_previous_page(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data['page_num'] > 0:
            data['page_num'] -= 1
            kb = await get_songs_list_kb(await db.get_user_songs_list(data['friend_id'], data['page_num']),
                                         data['page_num'] + 1, data['page_total'])
            await call.message.edit_reply_markup(kb)
