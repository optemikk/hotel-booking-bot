from aiogram.fsm.state import State, StatesGroup


class AddPlaceStates(StatesGroup):
    place_name = State()