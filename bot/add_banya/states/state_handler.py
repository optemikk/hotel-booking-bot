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

from bot.add_banya.states.states import AddBanyaStates
from bot.menu.states.states_kb import get_places_kb
from bot.add_banya.states.states_kb import get_add_cancel_kb, get_confirm_add_banya_kb


# <- bot.menu.callback.callback_handler

@menu_router.message(AddBanyaStates.banya_name)
async def process(msg: Message, state: FSMContext):
    await msg.delete()

    data = await state.get_data()
    prev_msg: Message = data['prev_msg']

    await bot_db.set_add_name(user_id=msg.from_user.id, name=msg.text, arg='banya')

    await state.clear()
    prev_msg = await prev_msg.edit_text(text='<b>✏ Введите цену и описание бани:</b>',
                                        reply_markup=await get_add_cancel_kb())

    await state.set_state(AddBanyaStates.banya_desc)
    await state.update_data(data={'prev_msg': prev_msg})


@menu_router.message(AddBanyaStates.banya_desc)
async def process(msg: Message, state: FSMContext):
    await msg.delete()

    data = await state.get_data()
    prev_msg: Message = data['prev_msg']

    await bot_db.set_add_desc(user_id=msg.from_user.id, desc=msg.text, arg='banya')

    await state.clear()
    await prev_msg.edit_text(text='<b>✏ Напишите контакты:</b>',
                             reply_markup=await get_add_cancel_kb())

    await state.set_state(AddBanyaStates.banya_contacts)
    await state.update_data(data={'prev_msg': prev_msg})


@menu_router.message(AddBanyaStates.banya_contacts)
async def process(msg: Message, state: FSMContext):
    await msg.delete()

    data = await state.get_data()
    prev_msg: Message = data['prev_msg']

    await bot_db.set_add_contacts(user_id=msg.from_user.id, contacts=msg.text, arg='banya')

    await state.clear()
    await prev_msg.edit_text(text='<b>✏ Отправьте фото вашей бани:</b>',
                             reply_markup=await get_add_cancel_kb())

    await state.set_state(AddBanyaStates.banya_photo)
    await state.update_data(data={'prev_msg': prev_msg})


@menu_router.message(AddBanyaStates.banya_photo)
async def process(msg: Message, state: FSMContext):
    data = await state.get_data()
    prev_msg: Message = data['prev_msg']

    try:
        file_id = msg.document.file_id
    except:
        file_id = msg.photo[0].file_id
    await bot_db.set_add_photo(user_id=msg.from_user.id, path=file_id, arg='banya')
    data = await bot_db.get_user_data_banya(msg.from_user.id)
    place, name, desc, contacts, photo = data
    await prev_msg.delete()
    await msg.answer_photo(caption='❔ <b>Ваша заявка на добавление бани:</b>\n\n'
                                   f'⛺ <i>Поселок: {place}\n'
                                   f'🔎 Название: {name}\n'
                                   f'📕 Описание и цена: {desc}\n'
                                   f'👤 Контакты: {contacts}\n'
                                   f'🌇 Фото: *сверху*\n\n</i>'
                                   '<b>Все верно?</b>',
                           photo=photo,
                           reply_markup=await get_confirm_add_banya_kb())
    await state.clear()
    await msg.delete()