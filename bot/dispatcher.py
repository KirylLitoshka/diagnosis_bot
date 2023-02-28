from bot.commands import set_bot_commands
from bot.fsm_states import Profile
from bot.handlers import *


async def on_startup(dispatcher):
    await set_bot_commands(dispatcher)
    dispatcher.register_message_handler(
        process_start, commands=["start"], state="*")
    dispatcher.register_message_handler(
        prev_state_handler, lambda msg: msg.text == "⬅️ Назад", state="*")
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
    dispatcher.register_message_handler(
        process_time_selection, state=Profile.time)
    dispatcher.register_message_handler(
        process_contact_submit, state=Profile.contact)
    dispatcher.register_message_handler(
        process_summary_message, state="summary"
    )


async def on_shutdown(dispatcher):
    dispatcher.stop_polling()
    await dispatcher.wait_closed()
