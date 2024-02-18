import aiogram
from aiogram import types
from bot.add_hotel.loader import add_hotel_router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram import F

from bot.main_loader import tgbot
from database.bot_database import bot_db

from bot.add_hotel.commands.command_kb import get_places_kb
from bot.add_hotel.states.states_kb import get_add_cancel_kb, confirm_admin_add_hotel_kb
from bot.add_hotel.states.states import AddHotelStates

from bot.start.commands.command_kb import get_start_kb


@add_hotel_router.callback_query(F.data == 'add-hotel')
async def process(callback: CallbackQuery):
    await callback.message.edit_text(text='<b>✏ Выберите поселок для вашего отеля.</b>',
                                     reply_markup=await get_places_kb())


@add_hotel_router.callback_query(F.data[:8] == 'h-place|')
async def process(callback: CallbackQuery, state: FSMContext):
    prev_msg = await callback.message.edit_text(text='<b>✏ Введите название своего отеля.</b>',
                                                reply_markup=await get_add_cancel_kb())
    await bot_db.set_add_place(user_id=callback.from_user.id, place=callback.data.split('|')[-1], arg='hotel')
    await state.set_state(AddHotelStates.hotel_name)
    await state.update_data(data={'prev_msg': prev_msg})


@add_hotel_router.callback_query(F.data == 'cancel-add-hotel')
async def process(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='<b>✅ Введенные данные были удалены, заявка отменена.</b>')


@add_hotel_router.callback_query(F.data == 'confirm-add-hotel')
async def process(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    data = await bot_db.get_user_data_hotel(callback.from_user.id)
    hotel_place, hotel_name, hotel_desc, hotel_contacts, hotel_photo = data
    media = [InputMediaPhoto(media=file_id) for file_id in hotel_photo.split('|')]
    await tgbot.send_media_group(chat_id=972383332,
                                 media=media)
    await tgbot.send_message(chat_id=972383332,
                             text='❔ <b>Новая заявка на добавление отеля:</b>\n\n'
                                  f'⛺ <i>Поселок: {hotel_place}\n'
                                  f'🔎 Название: {hotel_name}\n'
                                  f'📕 Описание и цена: {hotel_desc}\n'
                                  f'👤 Контакты: {hotel_contacts}\n'
                                  f'🌇 Фото: *сверху*</i>\n\n'
                                  f'👤 Пользователь: <a href="{callback.from_user.url}">{callback.from_user.full_name}</a>',
                             reply_markup=await confirm_admin_add_hotel_kb(callback.from_user.id))
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='<b>✅ Заявка была отправлена на рассмотрение. Мы оповестим вас, когда ее рассмотрят.</b>\n\n')


@add_hotel_router.callback_query(F.data[:14] == 'allow-posting|')
async def process(callback: CallbackQuery):
    user_id = int(callback.data.split("|")[-1])
    await bot_db.set_user_howner(user_id)
    await callback.message.edit_text(text=f'<b>Вы одобрили заявку <a href="tg://user?id={user_id}">пользователя</a></b>')
    await tgbot.send_message(chat_id=user_id,
                             text='<b>Вашу заявку одобрили! Можете начинать публиковать ваши отели</b>\n\n'
                                  '<i>Нажмите на /start, у вас появится новое меню для публикации</i>')


@add_hotel_router.callback_query(F.data[:15] == 'cancel-posting|')
async def process(callback: CallbackQuery):
    user_id = int(callback.data.split("|")[-1])
    await callback.message.edit_text(text=f'<b>Вы отменили заявку <a href="tg://user?id={user_id}">пользователя</a></b>')
    await tgbot.send_message(chat_id=user_id,
                             text='<b>Вашу заявку отклонили. Свяжитесь с администрацией для уточнения причин</b>')


@add_hotel_router.callback_query(F.data[:18] == 'confirm-adm-hotel|')
async def process(callback: CallbackQuery):
    user_id = int(callback.data.split('|')[-1])

    await bot_db.add_hotel(user_id)
    await tgbot.send_message(chat_id=user_id,
                             text='<b>Ваш отель опубликовали!</b>')

    await callback.message.delete()
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='<b>Вы успешно добавили отель!</b>')


@add_hotel_router.callback_query(F.data[:17] == 'cancel-adm-hotel|')
async def process(callback: CallbackQuery):
    user_id = int(callback.data.split('|')[-1])

    await tgbot.send_message(chat_id=user_id,
                             text='<b>Вашу заявку на публикацию отеля отклонили.\nСвяжитесь с администрацией для уточнения причины</b>')

    await callback.message.delete()
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='<b>Вы успешно отклонили отель!</b>')