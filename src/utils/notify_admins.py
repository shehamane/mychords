import logging

from aiogram import Dispatcher

from data.config import ADMIN_ID

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,
                    )


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(ADMIN_ID, "Бот Запущен")

    except Exception as err:
        logging.exception(err)
