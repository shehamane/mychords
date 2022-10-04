from aiogram.dispatcher.filters.state import StatesGroup, State


class Subscriptions(StatesGroup):
    SubscriptionsList = State()
    SubscriptionsSong = State()
    SubscriptionsCovers = State()
    SubscriptionAddition = State()
    SubscriptionsInfo = State()
