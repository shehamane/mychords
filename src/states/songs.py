from aiogram.dispatcher.filters.state import StatesGroup, State


class SongLoading(StatesGroup):
    FileRequest = State()
    FormationRequest = State()


class SongList(StatesGroup):
    SongList = State()
    SongInfo = State()
    SongChords = State()
    SongCovers = State()


class SongDeletion(StatesGroup):
    DeletionConfirmation = State()
