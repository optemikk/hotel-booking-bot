from aiogram import types
from aiogram.filters import Command
from bot.main_loader import tgbot


from bot.menu.states.states_kb import get_places_kb
from bot.start.commands.command_kb import get_start_kb

from bot.add_transfer.loader import add_transfer_router
from bot.add_transfer.commands.command_kb import get_places_kb, get_allow_posting_kb

from bot.add_transfer.commands.command_kb import get_calendar_kb

from database.bot_database import bot_db






@add_transfer_router.message(Command('trans'))
async def process(msg: types.Message):
    await msg.delete()
    await msg.answer(text='календар',
                     reply_markup=await get_calendar_kb())