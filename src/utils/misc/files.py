from aiogram.types import Audio, Voice
from pydub import AudioSegment
from os import remove

from data.structure_config import AUDIO_DIR_PATH
from utils.db_api.api import db_api as db


async def get_audio_path_by_id(song_id):
    song = await db.get_song(song_id)
    return f'{AUDIO_DIR_PATH}/{song.name} - {song.author}.wav'


async def get_cover_path_by_id(cover_id):
    cover = await db.get_cover(cover_id)
    return f'{AUDIO_DIR_PATH}/cover{cover.id}.wav'


async def is_correct_filename(fn):
    return fn[-4:] == '.mp3' and ' - ' in fn and len(fn.split(' - ')) == 2


async def convert_to_wav(path):
    AudioSegment.from_mp3(path).export(path[:-3] + 'wav', format='wav')
    remove(path)
    return path[:-3] + 'wav'


async def download_audio(audio: Audio):
    if not is_correct_filename(audio.file_name):
        return False, False, False, False
    await audio.download(AUDIO_DIR_PATH + audio.file_name)
    file_name = await convert_to_wav(AUDIO_DIR_PATH + audio.file_name)
    name, author = audio.file_name.split(' - ')
    author = author[:-4]
    duration = audio.duration

    return name, author, duration, file_name
