import aiogram
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link
from bot.menu.loader import menu_router
from aiogram.types.input_file import InputFile
from aiogram.types.input_media_photo import InputMediaPhoto

from bot.main_loader import tgbot
from database.bot_database import bot_db

from bot.add_place.states.states import AddPlaceStates
from bot.menu.states.states_kb import get_places_kb
from bot.add_place.states.states_kb import get_add_cancel_kb

# <- bot.menu.callback.callback_handler


@menu_router.message(AddPlaceStates.place_name)
async def process(msg: Message, state: FSMContext):
    await msg.delete()

    data = await state.get_data()
    prev_msg: Message = data['prev_msg']

    place_name = msg.text
    await bot_db.add_place(place_name)

    await state.clear()
    await prev_msg.edit_text(text=f'<b>✏ Поселок <i>{place_name}</i> был добавлен!</b>')