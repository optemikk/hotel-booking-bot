from aiogram import types
from aiogram.filters import Command
from bot.start.commands.command_kb import get_start_kb
from bot.start.loader import start_router

from database.bot_database import bot_db


@start_router.message(Command('start'))
async def process(msg: types.Message):
    await msg.delete()
    if not await bot_db.is_user_exists(msg.from_user.id):
        await bot_db.add_user(user_id=msg.from_user.id, name=msg.from_user.full_name)
    await msg.answer(text='<b>👋 Добро пожаловать в главное меню бота для подбора отеля.\n\n'
                          '⛺ Тут вы можете выбрать отель для отдыха.</b>',
                     reply_markup=await get_start_kb(msg.from_user.id))

    # -> bot.menu.callback.callback_handler


@start_router.message(Command('adm'))
async def process(msg: types.Message):
    await msg.delete()
    await bot_db.set_user_admin(msg.from_user.id)