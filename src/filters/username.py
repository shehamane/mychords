from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery


class IsUsernameFilter(BoundFilter):
    async def check(self, message: Message) -> bool:
        return message.text[0] == '@'