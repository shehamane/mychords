from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
import autochord

from keyboards.inline.formations import formations_kb
from loader import dp
from states import SongLoading
from utils.callback_datas import choose_formation_cd
from utils.db_api.api import db_api as db
from utils.misc.files import download_audio
from utils.misc.time import seconds_to_time


@dp.message_handler(Text(ignore_case=True, contains=['загрузить песню']), state='*')
async def get_audio_file(message: Message, state: FSMContext):
    await state.finish()
    text = 'Загрузите аудио, имя файла должно быть в формате "АВТОР - НАЗВАНИЕ.mp3".'

    async with state.proxy() as data:
        data['pinned_msg'] = await message.answer(text=text)
    await SongLoading.FileRequest.set()


@dp.message_handler(content_types=['audio'], state=SongLoading.FileRequest)
async def get_formation(message: Message, state: FSMContext):
    async with state.proxy() as data:
        name, author, duration, filename = await download_audio(message.audio)
        if not name:
            await data['pinned_msg'].edit_text('Имя файла не соотвутсвует требованиям. Попробуйте еще раз')
            return
        data['name'] = name
        data['author'] = author
        data['duration'] = seconds_to_time(duration)
        data['filename'] = filename

    text = 'Укажите гитарный строй:'
    await data['pinned_msg'].edit_text(text, reply_markup=formations_kb)
    await SongLoading.FormationRequest.set()


@dp.message_handler(content_types=['document'], state=SongLoading.FileRequest)
async def retry_to_get_audio_file(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['pinned_msg'].edit_text('Этот формат аудио не поддерживается.')


@dp.callback_query_handler(choose_formation_cd.filter(), state=SongLoading.FormationRequest)
async def load_song(call: CallbackQuery, callback_data: dict, state: FSMContext):
    user = await db.get_current_user()
    async with state.proxy() as data:
        song = await db.create_song(user.id, data['name'], data['author'],
                                    data['duration'], data['filename'],
                                    callback_data.get('formation'))
        await load_chords(song.id)
        await data['pinned_msg'].edit_text('Песня успешно загружена!', reply_markup=None)

    await state.finish()


async def load_chords(song_id):
    song = await db.get_song(song_id)
    chords = autochord.recognize(song.file_name)
    for start, end, name in chords:
        await db.create_chord(song_id, name, start, end)
