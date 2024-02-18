import aiogram
from aiogram import types
from bot.add_transfer.loader import add_transfer_router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link
from aiogram import F

from bot.main_loader import tgbot
from database.bot_database import bot_db

from bot.add_transfer.commands.command_kb import get_places_kb, get_calendar_kb
from bot.add_transfer.states.states_kb import get_add_cancel_kb, confirm_admin_add_tranfser_kb
from bot.add_transfer.states.states import AddTransferStates

from bot.start.commands.command_kb import get_start_kb


@add_transfer_router.callback_query(F.data == 'add-transfer')
async def process(callback: CallbackQuery):
    await callback.message.edit_text(text='<b>✏ Выберите поселок откуда вы предоставляете трансфер.</b>',
                                     reply_markup=await get_places_kb())


@add_transfer_router.callback_query(F.data[:8] == 't-place|')
async def process(callback: CallbackQuery, state: FSMContext):
    prev_msg = await callback.message.edit_text(text='<b>✏ Введите название своей кампании.</b>',
                                                reply_markup=await get_add_cancel_kb())
    await bot_db.set_add_place(user_id=callback.from_user.id, place=callback.data.split('|')[-1], arg='transfer')
    await state.set_state(AddTransferStates.transfer_name)
    await state.update_data(data={'prev_msg': prev_msg})
    await state.set_state(AddTransferStates.transfer_name)


@add_transfer_router.callback_query(F.data == 'cancel-add-trans')
async def process(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='<b>✅ Введенные данные были удалены, заявка отменена.</b>')


@add_transfer_router.callback_query(F.data == 'confirm-add-trans')
async def process(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    data = await bot_db.get_user_data_transfer(callback.from_user.id)
    place, name, desc, contacts, photo = data
    await tgbot.send_photo(chat_id=972383332,
                           caption='❔ <b>Новая заявка на добавление трансфера:</b>\n\n'
                                   f'⛺ <i>Поселок: {place}\n'
                                   f'🔎 Название: {name}\n'
                                   f'📕 Описание и цена: {desc}\n'
                                   f'👤 Контакты: {contacts}\n'
                                   f'🌇 Фото: *сверху*</i>\n\n'
                                   f'👤 Пользователь: <a href="{callback.from_user.url}">{callback.from_user.full_name}</a>',
                           photo=photo,
                           reply_markup=await confirm_admin_add_tranfser_kb(callback.from_user.id))
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='<b>✅ Заявка была отправлена на рассмотрение. Мы оповестим вас, когда ее рассмотрят.</b>\n\n')


@add_transfer_router.callback_query(F.data[:18] == 'confirm-adm-trans|')
async def process(callback: CallbackQuery):
    user_id = int(callback.data.split('|')[-1])

    await bot_db.add_transfer(user_id)
    await tgbot.send_message(chat_id=user_id,
                             text='<b>Ваш трансфер опубликовали!</b>')

    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='<b>Вы успешно добавили трансфер!</b>')
    await callback.message.delete()


@add_transfer_router.callback_query(F.data[:17] == 'cancel-adm-trans|')
async def process(callback: CallbackQuery):
    user_id = int(callback.data.split('|')[-1])

    await tgbot.send_message(chat_id=user_id,
                             text='<b>Вашу заявку на публикацию трансфера отклонили.\nСвяжитесь с администрацией для уточнения причины</b>')

    await callback.message.delete()
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='<b>Вы успешно отклонили трансфер!</b>')


@add_transfer_router.callback_query(F.data[:10] == 'trans-cal|')
async def process(callback: CallbackQuery):
    await callback.message.edit_text(text='каледарь',
                                     reply_markup=await get_calendar_kb(offset=int(callback.data.split('|')[-1])))