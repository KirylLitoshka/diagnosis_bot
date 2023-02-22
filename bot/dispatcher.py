from bot.handlers import *
from bot.fsm_states import Profile


async def on_startup(dispatcher):
    dispatcher.register_message_handler(
        process_start, commands=["start"], state="*")
    dispatcher.register_message_handler(
        process_city_selection, state=Profile.city)
    dispatcher.register_message_handler(
        process_device_type_selection, state=Profile.device_type)
    dispatcher.register_message_handler(
        process_manufacturer_selection, state=Profile.manufacturer)
    dispatcher.register_message_handler(
        process_defect_type_selection, state=Profile.defect_type)
    dispatcher.register_message_handler(
        process_defect_reason_selection, state=Profile.defect_reason)
    dispatcher.register_message_handler(
        process_date_selection, state=Profile.date)


async def on_shutdown(dispatcher):
    dispatcher.stop_polling()
    await dispatcher.wait_closed()
