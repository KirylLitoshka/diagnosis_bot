from aiogram import types


async def set_bot_commands(dispatcher): 
    await dispatcher.bot.set_my_commands(
        [
            types.BotCommand("start", "Поехали!"),
        ]
    )
