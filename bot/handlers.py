from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.fsm_states import Profile
from bot.vars import CITIES, DEVICE_TYPES, MANUFACTURERS, DEFECT_TYPES


__all__ = [
    "process_start",
    "process_city_selection",
    "process_device_type_selection",
    "process_manufacturer_selection",
    "process_defect_type_selection",
    "process_defect_reason_selection",
    "process_date_selection"
]


async def process_start(message: types.Message, state: FSMContext):
    text_message = "Приветсвенное сообщение\nУкажите Ваш город:"
    await Profile.city.set()
    await message.answer(
        text=text_message,
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(item)] for item in CITIES],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


async def process_city_selection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["selected_city"] = message.text
    await Profile.next()
    await message.answer(
        text="Укажите тип устройства",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(item)] for item in DEVICE_TYPES],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


async def process_device_type_selection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["device_type"] = message.text
    await Profile.next()
    await message.answer(
        text="Укажите фирму производителя",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(item)] for item in MANUFACTURERS],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


async def process_manufacturer_selection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["manufacturer"] = message.text
    await Profile.next()
    await message.answer(
        text="Укажите тип неисправности",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(item['name'])] for item in DEFECT_TYPES
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


async def process_defect_type_selection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["defect_type"] = message.text
    selected_defect_object = next(
        (item for item in DEFECT_TYPES if item["name"] == message.text), []
    )
    defect_reasons = selected_defect_object["reasons"]
    if not defect_reasons:
        await Profile.date.set()
        await message.answer(
            text="Укажите когда Вам удобно принять мастера",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(item)] for item in ["a", "b", "c"]
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
    else:
        await Profile.next()
        await message.answer(
            text="Укажите точнее",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(item)] for item in defect_reasons
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

async def process_defect_reason_selection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["defect_reason"] = message.text
    await Profile.next()
    await message.answer(
        text="Укажите когда Вам удобно принять мастера",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(item)] for item in ["a", "b", "c"]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


async def process_date_selection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if "defect_reason" not in data:
            data["defect_reason"] = None
        data["date"] = message.text
        await message.answer(str(data))