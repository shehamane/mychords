from aiogram import Dispatcher


def setup(dp: Dispatcher):
    from .is_user import IsNotUserFilter
    text_messages = [
        dp.message_handlers,
        dp.edited_message_handlers,
        dp.channel_post_handlers,
        dp.edited_channel_post_handlers,
    ]

    callback_messages = [
        dp.callback_query_handlers,
    ]

    dp.filters_factory.bind(IsNotUserFilter, event_handlers=text_messages)
