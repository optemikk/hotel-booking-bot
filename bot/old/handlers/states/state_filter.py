from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext


class SearchStateFiler(Filter):
    def __init__(self, msg_data: str):
        self.msg_data = msg_data

    def __call__(self, msg: Message, state: FSMContext):
        await state.clear()
        current_state = await self.get_state(self.msg_data.chat.id).get_state()
        return current_state == 'some_state'

