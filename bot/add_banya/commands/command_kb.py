from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.bot_database import bot_db


async def get_places_kb():
    places = await bot_db.get_all_places()
    keyboard = [
        [InlineKeyboardButton(text=place[0], callback_data=f'b-place|{place[0]}')] for place in places
    ]
    keyboard.append([InlineKeyboardButton(text='❌ Отменить', callback_data='cancel-search')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_allow_posting_kb(user_id):
    keyboard = [
        [InlineKeyboardButton(text='✅ Разрешить', callback_data=f'allow-posting|{user_id}'),
         InlineKeyboardButton(text='❌ Отменить', callback_data=f'cancel-posting|{user_id}')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)