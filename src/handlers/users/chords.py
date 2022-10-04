from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, InputFile

from data.structure_config import IMG_DIR_PATH, IMG_FORMAT
from keyboards.inline.chords import get_chords_kb
from states.songs import SongList

from loader import dp
from utils.callback_datas import view_chords_cd
from utils.db_api.api import db_api as db
from utils.misc.img import concat_images


@dp.callback_query_handler(view_chords_cd.filter(), state=SongList.all_states)
async def show_chords(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    song_id = int(callback_data['song_id'])
    async with state.proxy() as data:
        data['chords_song_id'] = song_id
        data['page_num'] = 0
        data['page_total'] = await db.count_chords_list_pages(song_id) + 1
        chords = await db.get_chords_list(song_id, 0)
        pathes = [IMG_DIR_PATH + chord.name + IMG_FORMAT for chord in chords]
        img_path = await concat_images(pathes)
        data['pinned_msg'] = await call.message.answer_photo(InputFile(img_path),
                                                             caption=' '.join([chord.name for chord in chords]),
                                                             reply_markup=await get_chords_kb(1, data['page_total']))
    await SongList.SongChords.set()


@dp.callback_query_handler(text='next', state=SongList.SongChords)
async def show_next_page(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data['page_num'] < await db.count_chords_list_pages(data['chords_song_id']):
            data['page_num'] += 1
            kb = await get_chords_kb(data['page_num'] + 1, data['page_total'])
            chords = await db.get_chords_list(data['chords_song_id'], data['page_num'])
            pathes = [IMG_DIR_PATH + chord.name + IMG_FORMAT for chord in chords]
            img_path = await concat_images(pathes)
            await data['pinned_msg'].edit_media(InputMediaPhoto(InputFile(img_path)))
            await data['pinned_msg'].edit_caption(caption=' '.join([chord.name for chord in chords]),
                                                  reply_markup=kb)


@dp.callback_query_handler(text='previous', state=SongList.SongChords)
async def show_previous_page(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data['page_num'] > 0:
            data['page_num'] -= 1
            kb = await get_chords_kb(data['page_num'] + 1, data['page_total'])
            chords = await db.get_chords_list(data['chords_song_id'], data['page_num'])
            pathes = [IMG_DIR_PATH + chord.name + IMG_FORMAT for chord in chords]
            img_path = await concat_images(pathes)
            await data['pinned_msg'].edit_media(InputMediaPhoto(InputFile(img_path)))
            await data['pinned_msg'].edit_caption(caption=' '.join([chord.name for chord in chords]),
                                                  reply_markup=kb)
