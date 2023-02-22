from aiogram import Dispatcher, Bot, executor
from aiogram.contrib.fsm_storage.files import JSONStorage
from bot.dispatcher import on_startup, on_shutdown
from bot.settings import STORAGE


def start_bot():
    bot = Bot("")
    dispatcher = Dispatcher(bot, storage=JSONStorage(STORAGE))
    executor.start_polling(
        dispatcher=dispatcher,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
