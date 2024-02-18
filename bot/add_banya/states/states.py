from aiogram.fsm.state import State, StatesGroup


class AddBanyaStates(StatesGroup):
    banya_name = State()
    banya_desc = State()
    banya_contacts = State()
    banya_photo = State()