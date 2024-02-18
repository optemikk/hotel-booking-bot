import aiogram
from aiogram import types
from bot.add_hotel.loader import add_hotel_router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link
from aiogram import F

from bot.main_loader import tgbot
from database.bot_database import bot_db

from bot.add_place.states.states_kb import get_add_cancel_kb
from bot.add_place.states.states import AddPlaceStates

from bot.start.commands.command_kb import get_start_kb


@add_hotel_router.callback_query(F.data == 'add-place')
async def process(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddPlaceStates.place_name)
    prev_msg = await callback.message.edit_text(text='<b>✏ Введите название поселка</b>',
                                                reply_markup=await get_add_cancel_kb())
    await state.update_data(data={'prev_msg': prev_msg})


@add_hotel_router.callback_query(F.data == 'cancel-add-place')
async def process(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='<b>✅ Введенные данные были удалены, заявка отменена.</b>')
