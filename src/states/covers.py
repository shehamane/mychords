from aiogram.dispatcher.filters.state import StatesGroup, State


class CoverLoading(StatesGroup):
    VoiceRequest = State()
    NameRequest = State()
