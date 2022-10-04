from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, InputFile

from keyboards.inline import confirmation_kb
from keyboards.inline.songs import get_songs_list_kb, get_song_info_kb
from states.songs import SongList, SongDeletion
from utils.callback_datas import choose_song_cd, delete_song_cd, send_song_cd

from loader import dp
from utils.db_api.api import db_api as db
from utils.misc.files import get_audio_path_by_id


@dp.message_handler(Text(ignore_case=True, contains=['мои песни']), state='*')
async def show_songs_list(message: Message, state: FSMContext):
    await state.finish()

    user = await db.get_current_user()
    async with state.proxy() as data:
        data['page_num'] = 0
        data['page_total'] = await db.count_user_songs_list_pages(user.id) + 1

        kb = await get_songs_list_kb(await db.get_user_songs_list(user.id, 0), 1, data['page_total'])
        await message.answer('Ваши песни:', reply_markup=kb)
    await SongList.SongList.set()


@dp.callback_query_handler(text='next', state=SongList.SongList)
async def show_next_page(call: CallbackQuery, state: FSMContext):
    user = await db.get_current_user()
    async with state.proxy() as data:
        if data['page_num'] < await db.count_user_songs_list_pages(user.id):
            data['page_num'] += 1
            kb = await get_songs_list_kb(await db.get_user_songs_list(user.id, data['page_num']),
                                         data['page_num'] + 1, data['page_total'])
            await call.message.edit_reply_markup(kb)
    await SongList.SongList.set()


@dp.callback_query_handler(text='previous', state=SongList.SongList)
async def show_previous_page(call: CallbackQuery, state: FSMContext):
    user = await db.get_current_user()
    async with state.proxy() as data:
        if data['page_num'] > 0:
            data['page_num'] -= 1
            kb = await get_songs_list_kb(await db.get_user_songs_list(user.id, data['page_num']),
                                         data['page_num'] + 1, data['page_total'])
            await call.message.edit_reply_markup(kb)
    await SongList.SongList.set()


@dp.callback_query_handler(choose_song_cd.filter(), state=SongList.all_states)
async def show_song_info(call: CallbackQuery, callback_data: dict):
    song = await db.get_song(int(callback_data.get('song_id')))
    text = f"Название: {song.name}\n" \
           f"Автор: {song.author}\n" \
           f"Длительность: {song.duration}"
    await call.message.answer(text, reply_markup=await get_song_info_kb(song.id))
    await SongList.SongInfo.set()


@dp.callback_query_handler(delete_song_cd.filter(), state=SongList.all_states)
async def delete_song(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['song_to_delete_id'] = int(callback_data['song_id'])
    await call.message.edit_text('Вы уверены?', reply_markup=confirmation_kb)
    await SongDeletion.DeletionConfirmation.set()


@dp.callback_query_handler(text='no', state=SongDeletion.DeletionConfirmation)
async def show_song_info(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        song = await db.get_song(data['song_to_delete_id'])
        del data['song_to_delete_id']

    text = f"Название: {song.name}\n" \
           f"Автор: {song.author}\n" \
           f"Длительность: {song.duration}"
    await call.message.edit_text(text, reply_markup=await get_song_info_kb(song.id))
    await SongList.SongInfo.set()


@dp.callback_query_handler(text='yes', state=SongDeletion.DeletionConfirmation)
async def delete_song(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await db.delete_song(int(data['song_to_delete_id']))
        del data['song_to_delete_id']
    await call.message.edit_text('Песня удалена')
    await SongList.SongList.set()


@dp.callback_query_handler(send_song_cd.filter(), state=SongList.all_states)
async def send_song(call: CallbackQuery, callback_data: dict):
    song_id = int(callback_data['song_id'])
    await call.message.answer_audio(InputFile(await get_audio_path_by_id(song_id)))
