from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.bot_database import bot_db


async def get_start_kb(user_id: int = 0):
    keyboard = list()
    admin = False
    howner = False
    if await bot_db.is_user_exists(user_id):
        if await bot_db.is_user_admin(user_id):
            admin = True
        if await bot_db.is_user_howner(user_id):
            howner = True
    if admin:
        keyboard.append([InlineKeyboardButton(text='🏘️ Все отели', callback_data='all-hotels|0'),
                         InlineKeyboardButton(text='🏘️ Все поселки', callback_data='all-places|0'),
                         InlineKeyboardButton(text='🗺️ Все трансферы', callback_data='all-trans|0')])
        keyboard.append([InlineKeyboardButton(text='👤 Пользователи', callback_data='all-users|0')])
    if howner:
        keyboard.append([InlineKeyboardButton(text='⛺ Мои отели', callback_data='my-hotels'),
                         InlineKeyboardButton(text='♨️ Мои бани', callback_data='my-banya'),
                         InlineKeyboardButton(text='🗺️ Мой трансфер', callback_data='my-transfer')])
    keyboard.append([InlineKeyboardButton(text='🔎 Найти отель', callback_data='search'),
                     InlineKeyboardButton(text='♨️ Найти баню', callback_data='banya'),
                    InlineKeyboardButton(text='🗺️ Трансфер', callback_data='transfer')])
    keyboard.append([InlineKeyboardButton(text='👤 Контакты', callback_data='contacts')])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)