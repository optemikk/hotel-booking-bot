from aiogram.filters import Filter
from aiogram.types import CallbackQuery


class SearchFiler(Filter):
    def __init__(self, callback_data: str):
        self.callback_data = callback_data

    def __call__(self, callback: CallbackQuery):
        return self.callback_data == 'search'