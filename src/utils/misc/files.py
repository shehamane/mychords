from aiogram.types import Audio
from pydub import AudioSegment
from os import remove


async def is_correct_filename(fn):
    return fn[-4:] == '.mp3' and ' - ' in fn and len(fn.split(' - ')) == 2


async def convert_to_wav(path):
    AudioSegment.from_mp3(path).export(path[:-3] + 'wav', format='wav')
    remove(path)
    return path[:-3] + 'wav'


async def download_audio(audio: Audio):
    if not is_correct_filename(audio.file_name):
        return False, False, False, False
    await audio.download('audio/' + audio.file_name)
    file_name = await convert_to_wav('audio/' + audio.file_name)
    name, author = audio.file_name.split(' - ')
    author = author[:-4]
    duration = audio.duration

    return name, author, duration, file_name
