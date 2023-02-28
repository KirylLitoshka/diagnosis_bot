from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.files import JSONStorage

from bot.dispatcher import on_shutdown, on_startup
from bot.settings import STORAGE


def start_bot(token: str):
    bot = Bot(token=token)
    dispatcher = Dispatcher(bot, storage=JSONStorage(STORAGE))
    executor.start_polling(
        dispatcher=dispatcher,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
