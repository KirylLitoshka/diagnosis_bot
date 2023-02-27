import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.fsm_states import Profile
from bot.utils import get_date_range, get_time_range
from bot.vars import CITIES, DEFECT_TYPES, DEVICE_TYPES, MANUFACTURERS

__all__ = [
    "process_start",
    "process_city_selection",
    "process_device_type_selection",
    "process_manufacturer_selection",
    "process_defect_type_selection",
    "process_defect_reason_selection",
    "process_date_selection",
    "process_time_selection",
    "process_contact_submit",
    "prev_state_handler"
]


async def process_start(message: types.Message, state: FSMContext):
    await message.answer("Приветсвенное сообщение")
    await asyncio.sleep(1)
    return await send_city_selection(message, state)


async def send_city_selection(message: types.Message, state: FSMContext):
    await state.set_state(Profile.city)
    await message.answer(
        text="Укажите Ваш город:",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(item)] for item in CITIES],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


async def process_city_selection(message: types.Message, state: FSMContext):
    if message.text not in CITIES:
        return await message.delete()
    async with state.proxy() as data:
        data["selected_city"] = message.text
    return await send_device_type_selection(message, state)


async def send_device_type_selection(message: types.Message, state: FSMContext):
    await state.set_state(Profile.device_type)
    keyboard = [
        [types.KeyboardButton("Назад")], *[[types.KeyboardButton(item)] for item in DEVICE_TYPES]
    ]
    await message.answer(
        text="Укажите тип устройства",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


async def process_device_type_selection(message: types.Message, state: FSMContext):
    if message.text not in DEVICE_TYPES:
        return await message.delete()
    async with state.proxy() as data:
        data["device_type"] = message.text
    return await send_manufacturer_selection(message, state)


async def send_manufacturer_selection(message: types.Message, state: FSMContext):
    await state.set_state(Profile.manufacturer)
    keyboard = [
        [types.KeyboardButton("Назад")], *[[types.KeyboardButton(item)] for item in MANUFACTURERS]
    ]
    await message.answer(
        text="Укажите фирму производителя",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


async def process_manufacturer_selection(message: types.Message, state: FSMContext):
    if message.text not in MANUFACTURERS:
        return await message.delete()
    async with state.proxy() as data:
        data["manufacturer"] = message.text
    return await send_defect_type_selection(message, state)


async def send_defect_type_selection(message: types.Message, state: FSMContext):
    await state.set_state(Profile.defect_type)
    keyboard = [
        [types.KeyboardButton("Назад")], *[[types.KeyboardButton(item['name'])] for item in DEFECT_TYPES]
    ]
    await message.answer(
        text="Укажите тип неисправности",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
            row_width=50
        )
    )


async def process_defect_type_selection(message: types.Message, state: FSMContext):
    if message.text not in [defect["name"] for defect in DEFECT_TYPES]:
        return await message.delete()
    async with state.proxy() as data:
        data["defect_type"] = message.text
    defect = next(
        (item for item in DEFECT_TYPES if item["name"] == message.text), {}
    )
    defect_reasons = defect.get("reasons", None)
    if not defect_reasons:
        return await send_date_selection(message, state)
    return await send_reason_selection(message, state)


async def send_date_selection(message: types.Message, state: FSMContext):
    await state.set_state(Profile.date)
    keyboard = [
        [types.KeyboardButton("Назад")], *[[types.KeyboardButton(item)] for item in get_date_range()]
    ]
    await message.answer(
        text="Укажите дату когда Вам удобно принять мастера",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


async def send_reason_selection(message: types.Message, state: FSMContext):
    await state.set_state(Profile.defect_reason)
    async with state.proxy() as data:
        user_defect_type = data["defect_type"]
    defect = next(
        (item for item in DEFECT_TYPES if item["name"] == user_defect_type), {}
    )
    reasons = defect["reasons"]
    keyboard = [
        [types.KeyboardButton("Назад")], *[[types.KeyboardButton(item)] for item in reasons]
    ]
    await message.answer(
        text="Укажите подробнее",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


async def process_defect_reason_selection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["defect_reason"] = message.text
    return await send_date_selection(message, state)


async def process_date_selection(message: types.Message, state: FSMContext):
    if message.text not in get_date_range():
        return await message.delete()
    async with state.proxy() as data:
        if "defect_reason" not in data:
            data["defect_reason"] = None
        data["date"] = message.text
    await send_time_selection(message, state)


async def send_time_selection(message: types.Message, state: FSMContext):
    await state.set_state(Profile.time)
    keyboard = [
        [types.KeyboardButton("Назад")], *[[types.KeyboardButton(item)] for item in get_time_range()]
    ]
    await message.answer(
        text="Укажите удобное Вам время",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=keyboard,
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )


async def process_time_selection(message: types.Message, state: FSMContext):
    if message.text not in get_time_range():
        return await message.delete()
    async with state.proxy() as data:
        data["time"] = message.text
        username = message.from_user.mention
        if username.startswith("@"):
            data['contact'] = username
        state_data = data.as_dict()
    if state_data.get("contact"):
        return await send_final_message(message, state)
    return await send_contact_submit(message, state)


async def send_contact_submit(message: types.Message, state: FSMContext):
    await state.set_state(Profile.contact)
    await message.answer(
        text="Введите контактные данные для связи (mail, tel)"
    )


async def process_contact_submit(message: types. Message, state: FSMContext):
    async with state.proxy() as data:
        data["contact"] = message.text
    return await send_final_message(message, state)


async def send_final_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        output_data = data.as_dict()
    await state.finish()
    output_message = f"""
Итоговое сообщение (заменить текст)

Город: {output_data['selected_city']}
Тип устройства: {output_data['device_type']}
Фирма производителя: {output_data['manufacturer']}
Тип неисправности: {output_data['defect_type']}
Подробнее: {output_data['defect_reason']}
Дата: {output_data['date']}
Время: {output_data['time']}
"""
    await message.answer(output_message)
    await message.bot.send_message(
        chat_id=871840722, 
        text=output_message + f"\nКонтакт: {output_data['contact']}"
    )


async def prev_state_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        state_data = data.as_dict()
    current_state = await state.get_state()
    if current_state == "Profile:time":
        return await send_date_selection(message, state)
    elif current_state == "Profile:date":
        if state_data.get("defect_reason", None):
            return await send_reason_selection(message, state)
        return await send_defect_type_selection(message, state)
    elif current_state == "Profile:defect_reason":
        return await send_defect_type_selection(message, state)
    elif current_state == "Profile:defect_type":
        return await send_manufacturer_selection(message, state)
    elif current_state == "Profile:manufacturer":
        return await send_device_type_selection(message, state)
    elif current_state == "Profile:device_type":
        return await send_city_selection(message, state)
    else:
        return await message.delete()
