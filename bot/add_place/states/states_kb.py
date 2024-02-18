from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.bot_database import bot_db


async def get_add_cancel_kb():
    keyboard = [
        [InlineKeyboardButton(text='❌ Отменить', callback_data='cancel-add-place')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)