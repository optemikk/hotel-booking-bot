from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.bot_database import bot_db


async def get_places_kb():
    places = await bot_db.get_all_places()
    keyboard = [
        [InlineKeyboardButton(text=place[0], callback_data=f'trans-place|{place[0]}')] for place in places
    ]
    keyboard.append([InlineKeyboardButton(text='❌ Отменить', callback_data='cancel-search')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_add_cancel_kb():
    keyboard = [
        [InlineKeyboardButton(text='❌ Отменить', callback_data='cancel-add-trans')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_confirm_add_transfer_kb():
    keyboard = [
        [InlineKeyboardButton(text='✅ Подтвердить', callback_data='confirm-add-trans'),
         InlineKeyboardButton(text='❌ Отменить', callback_data='cancel-add-trans')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def confirm_admin_add_tranfser_kb(user_id: int):
    keyboard = [
        [InlineKeyboardButton(text='✅ Подтвердить', callback_data=f'confirm-adm-trans|{user_id}'),
         InlineKeyboardButton(text='❌ Отменить', callback_data=f'cancel-adm-trans|{user_id}')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)