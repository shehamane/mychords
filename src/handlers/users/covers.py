from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InputFile

from keyboards.inline.covers import get_covers_kb, get_cover_info_kb
from states.covers import CoverLoading
from states.songs import SongList

from loader import dp
from utils.callback_datas import new_cover_cd, get_covers_cd, choose_cover_cd, delete_cover_cd, \
    send_cover_cd
from utils.db_api.api import db_api as db
from utils.misc.accuracy import calculate_accuracy
from utils.misc.files import get_cover_path_by_id


@dp.callback_query_handler(new_cover_cd.filter(), state=SongList.all_states)
async def request_cover(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    song_id = int(callback_data['song_id'])
    async with state.proxy() as data:
        data['covered_song_id'] = song_id
    await call.message.answer('Запишите свой кавер в голосовом сообщении...')
    await CoverLoading.VoiceRequest.set()


@dp.message_handler(content_types=['voice'], state=CoverLoading.VoiceRequest)
async def request_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['voice_msg'] = message
    await message.answer('Назовите ваш кавер')
    await CoverLoading.NameRequest.set()


@dp.message_handler(content_types=['text'], state=CoverLoading.NameRequest)
async def create_cover(message: Message, state: FSMContext):
    user = await db.get_current_user()
    async with state.proxy() as data:
        cover = await db.create_cover(data['covered_song_id'], user.id, message.text)
        await data['voice_msg'].voice.download(cover.file_name)
        await cover.update(accuracy=await calculate_accuracy(cover.file_name, data['covered_song_id'])).apply()
    await message.answer(f'Кавер записан! Ваш результат: {cover.accuracy}%')
    await state.finish()


@dp.callback_query_handler(get_covers_cd.filter(), state=SongList.all_states)
async def get_song_covers(call: CallbackQuery, callback_data: dict):
    user = await db.get_current_user()
    song_id = int(callback_data['song_id'])
    covers = await db.get_user_song_covers(user.id, song_id)
    await call.message.edit_text('Ваши каверы:',
                                 reply_markup=await get_covers_kb(covers))
    await SongList.SongCovers.set()


@dp.callback_query_handler(choose_cover_cd.filter(), state=SongList.all_states)
async def show_cover_info(call: CallbackQuery, callback_data: dict):
    cover_id = int(callback_data['cover_id'])
    cover = await db.get_cover(cover_id)
    song = await db.get_song(cover.song_id)
    text = f'Кавер: {cover.name}\n' \
           f'Песня: {song.name} - {song.author}\n' \
           f'Схожесть: {cover.accuracy}%'
    await call.message.answer(text,
                              reply_markup=await get_cover_info_kb(cover_id))


@dp.callback_query_handler(delete_cover_cd.filter(), state=SongList.all_states)
async def delete_cover(call: CallbackQuery, callback_data: dict):
    cover_id = int(callback_data['cover_id'])
    cover = await db.get_cover(cover_id)
    await cover.delete()
    await call.message.edit_text('Кавер удален')
    await SongList.SongInfo.set()


@dp.callback_query_handler(send_cover_cd.filter(), state=SongList.all_states)
async def send_cover(call: CallbackQuery, callback_data: dict):
    cover_id = int(callback_data['cover_id'])
    await call.message.answer_audio(InputFile(await get_cover_path_by_id(cover_id)))
