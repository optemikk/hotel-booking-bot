import aiogram
from aiogram import types
from bot.add_banya.loader import add_banya_router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link
from aiogram import F

from bot.main_loader import tgbot
from database.bot_database import bot_db

from bot.add_banya.commands.command_kb import get_places_kb
from bot.add_banya.states.states_kb import get_add_cancel_kb, confirm_admin_add_banya_kb
from bot.add_banya.states.states import AddBanyaStates

from bot.start.commands.command_kb import get_start_kb


@add_banya_router.callback_query(F.data == 'add-banya')
async def process(callback: CallbackQuery):
    await callback.message.edit_text(text='<b>✏ Выберите поселок для вашей бани.</b>',
                                     reply_markup=await get_places_kb())


@add_banya_router.callback_query(F.data[:8] == 'b-place|')
async def process(callback: CallbackQuery, state: FSMContext):
    prev_msg = await callback.message.edit_text(text='<b>✏ Введите название своей бани.</b>',
                                                reply_markup=await get_add_cancel_kb())
    await bot_db.set_add_place(user_id=callback.from_user.id, place=callback.data.split('|')[-1], arg='banya')
    await state.set_state(AddBanyaStates.banya_name)
    await state.update_data(data={'prev_msg': prev_msg})


@add_banya_router.callback_query(F.data == 'cancel-add-banya')
async def process(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='<b>✅ Введенные данные были удалены, заявка отменена.</b>')


@add_banya_router.callback_query(F.data == 'confirm-add-banya')
async def process(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    data = await bot_db.get_user_data_banya(callback.from_user.id)
    hotel_place, hotel_name, hotel_desc, hotel_contacts, hotel_photo = data
    await tgbot.send_photo(chat_id=972383332,
                           caption='❔ <b>Новая заявка на добавление бани:</b>\n\n'
                                   f'⛺ <i>Поселок: {hotel_place}\n'
                                   f'🔎 Название: {hotel_name}\n'
                                   f'📕 Описание и цена: {hotel_desc}\n'
                                   f'👤 Контакты: {hotel_contacts}\n'
                                   f'🌇 Фото: *сверху*</i>\n\n'
                                   f'👤 Пользователь: <a href="{callback.from_user.url}">{callback.from_user.full_name}</a>',
                           photo=hotel_photo,
                           reply_markup=await confirm_admin_add_banya_kb(callback.from_user.id))
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='<b>✅ Заявка была отправлена на рассмотрение. Мы оповестим вас, когда ее рассмотрят.</b>\n\n')


@add_banya_router.callback_query(F.data[:18] == 'confirm-adm-banya|')
async def process(callback: CallbackQuery):
    user_id = int(callback.data.split('|')[-1])

    await bot_db.add_banya(user_id)
    await tgbot.send_message(chat_id=user_id,
                             text='<b>Вашу баню опубликовали!</b>')

    await callback.message.delete()
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='<b>Вы успешно добавили баню!</b>')


@add_banya_router.callback_query(F.data[:17] == 'cancel-adm-banya|')
async def process(callback: CallbackQuery):
    user_id = int(callback.data.split('|')[-1])

    await tgbot.send_message(chat_id=user_id,
                             text='<b>Вашу заявку на публикацию бани отклонили.\nСвяжитесь с администрацией для уточнения причины</b>')

    await callback.message.delete()
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='<b>Вы успешно отклонили баню!</b>')