from aiogram.dispatcher.filters.state import StatesGroup, State


class Profile(StatesGroup):
    city = State()
    device_type = State()
    manufacturer = State()
    defect_type = State()
    defect_reason = State()
    date = State()