from aiogram.dispatcher.filters.state import State, StatesGroup


class Profile(StatesGroup):
    city = State()
    device_type = State()
    manufacturer = State()
    defect_type = State()
    defect_reason = State()
    date = State()
    time = State()
    contact = State()
