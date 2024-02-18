from aiogram.fsm.state import State, StatesGroup


class AddTransferStates(StatesGroup):
    transfer_name = State()
    transfer_desc = State()
    transfer_contacts = State()
    transfer_photo = State()