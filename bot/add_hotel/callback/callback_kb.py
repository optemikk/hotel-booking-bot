from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_confirm_data_kb():
    keyboard = [
        [InlineKeyboardButton(text='✅ Подтвердить', callback_data='confirm-search'),
         InlineKeyboardButton(text='❌ Отменить', callback_data='cancel-search')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)