from aiogram.dispatcher.filters.state import StatesGroup, State


class SongLoading(StatesGroup):
    FileRequest = State()
    FormationRequest = State()