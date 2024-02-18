from aiogram.fsm.state import State, StatesGroup


class AddHotelStates(StatesGroup):
    hotel_name = State()
    hotel_desc = State()
    hotel_contacts = State()
    hotel_photo = State()