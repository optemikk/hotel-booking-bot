from aiogram.fsm.state import State, StatesGroup


class SearchState(StatesGroup):
    search_date = State()
    search_count = State()
    search_children = State()

    banya_date = State()
    banya_time = State()
    banya_count = State()

    transfer_time = State()
    transfer_count = State()
    transfer_children = State()
    transfer_data = State()