from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.bot_database import bot_db


async def get_places_kb():
    places = await bot_db.get_all_places()
    keyboard = [
        [InlineKeyboardButton(text=place[0], callback_data=f'banya-place|{place[0]}')] for place in places
    ]
    keyboard.append([InlineKeyboardButton(text='❌ Отменить', callback_data='cancel-search')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_add_cancel_kb():
    keyboard = [
        [InlineKeyboardButton(text='❌ Отменить', callback_data='cancel-add-banya')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_confirm_add_banya_kb():
    keyboard = [
        [InlineKeyboardButton(text='✅ Подтвердить', callback_data='confirm-add-banya'),
         InlineKeyboardButton(text='❌ Отменить', callback_data='cancel-add-banya')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def confirm_admin_add_banya_kb(user_id: int):
    keyboard = [
        [InlineKeyboardButton(text='✅ Подтвердить', callback_data=f'confirm-adm-banya|{user_id}'),
         InlineKeyboardButton(text='❌ Отменить', callback_data=f'cancel-adm-banya|{user_id}')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)