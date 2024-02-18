from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def start_kb():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔎 Поиск', callback_data='search')]
    ])
    return keyboard