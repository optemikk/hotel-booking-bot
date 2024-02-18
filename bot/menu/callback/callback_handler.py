import aiogram
from aiogram import types
from bot.menu.loader import menu_router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link
from aiogram import F

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.input_media_photo import InputMediaPhoto

from bot.main_loader import tgbot
from database.bot_database import bot_db

from bot.menu.callback.callback_kb import get_search_cancel_kb, get_confirm_data_kb,\
    get_confirm_request_hotel, get_confirm_hotel, get_hotels_kb, get_banya_cancel_kb, get_my_hotels_back_kb,\
    get_del_hotel_confirm_kb, get_confirm_banya_search_kb, get_banyas_kb, get_confirm_request_banya, get_confirm_banya,\
    get_confirm_date_keyboard, get_transfers_kb, get_confirm_place_kb, get_confirm_request_transfer, get_confirm_transfer,\
    get_all_hotels_kb, get_all_places_kb, get_all_transfers_kb, get_all_users_kb
from bot.menu.states.states_kb import get_places_kb
from bot.menu.states.states import SearchState
from bot.menu.states.states_kb import get_calendar_kb

from bot.start.commands.command_kb import get_start_kb



# @menu_router.callback_query(F.data)
# async def process(callback: CallbackQuery):
#     print(callback.data)


@menu_router.callback_query(F.data == 'start')
async def process(callback: CallbackQuery):
    await callback.message.edit_text(text='<b>👋 Добро пожаловать в главное меню бота для подбора отеля.\n\n'
                                          '⛺ Тут вы можете выбрать отель для отдыха.</b>',
                                     reply_markup=await get_start_kb(callback.from_user.id))


@menu_router.callback_query(F.data == 'banya')
async def process(callback: CallbackQuery):
    # await state.set_state(SearchState.banya_date)
    await callback.message.edit_text(text='<b>✏ Выберите дату посещения</b>',
                                     reply_markup=await get_calendar_kb(arg='banya'))

    # await state.update_data(data={'prev_msg': prev_msg})


@menu_router.callback_query(F.data == 'transfer')
async def process(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchState.transfer_data)
    prev_msg = await callback.message.edit_text(text='<b>✏ Введите сюда все пожелания и данные о вас для дальнейшего сотрудничества:</b>',
                                                reply_markup=await get_search_cancel_kb())
    await state.update_data(data={'prev_msg': prev_msg})


@menu_router.callback_query(F.data[:10] == 'banya-day|')
async def process(callback: CallbackQuery, state: FSMContext):
    await bot_db.update_user_date(user_id=callback.from_user.id, date=callback.data.split('|')[-1], arg='banya')
    prev_msg = await callback.message.edit_text(text='<b>✏ Введите время посещения</b>',
                                                reply_markup=await get_search_cancel_kb())
    await state.set_state(SearchState.banya_time)
    await state.update_data(data={'prev_msg': prev_msg})



@menu_router.callback_query(F.data == 'contacts')
async def process(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Контакты:\n\n*тут ваши контакты*',
                                     reply_markup=await get_start_kb(callback.from_user.id))



@menu_router.callback_query(F.data == 'search')
async def process(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchState.search_date)
    prev_msg = await callback.message.edit_text(text='<b>✏ Выберите даты проживания (с какого по какое)</b>',
                                                reply_markup=await get_calendar_kb(arg='hotel-from'))
    await state.update_data(data={'prev_msg': prev_msg})

    # -> bot.menu.states.state_handler


# <- bot.menu.states.state_handler


@menu_router.callback_query(F.data[:12] == 'banya-place|')
async def process(callback: CallbackQuery, state: FSMContext):
    place = callback.data.split('|')[-1]
    banyas = await bot_db.get_place_banyas(place)
    if not banyas:
        await callback.answer(text='❌ Бань не найдено!')
        return
    await bot_db.update_user_place(user_id=callback.from_user.id, place=place, arg='banya')
    data = await bot_db.get_user_data(callback.from_user.id)
    date = data[27]
    time = data[28]
    count = data[29]
    place = data[30]
    await callback.message.edit_text(text=f'<b>❔ Вы хотите найти баню в поселке <i>{place}</i>, '
                                          f'на <i>{count} человек</i> '
                                          f'в период <i>{date}</i> во время <i>{time}</i>?</b>\n\n'
                                          f'<i>Все верно?</i>',
                                     reply_markup=await get_confirm_banya_search_kb())


# @menu_router.callback_query(F.data[:13] == 'search-place|')
# async def process(callback: CallbackQuery, state: FSMContext):
#     # await callback.message.delete()
#
#     place = callback.data.split('|')[-1]
#     hotels = await bot_db.get_place_hotels(place)
#     if not hotels:
#         await callback.answer(text='❌ Отелей не найдено!')
#         return
#     await bot_db.update_user_place(user_id=callback.from_user.id, place=place, arg='hotel')
#     data = await bot_db.get_user_data(callback.from_user.id)
#     date = data[12]
#     time = data[13]
#     count = data[14]
#     place = data[15]
#     await callback.message.edit_text(text=f'<b>❔ Вы хотите найти отель в поселке <i>{place}</i>, '
#                                           f'на <i>{count} человек </i> '
#                                           f'в период <i>{date}</i> в <i>{time}</i>?</b>\n\n'
#                                           f'<i>Все верно?</i>',
#                                      reply_markup=await get_confirm_data_kb())



@menu_router.callback_query(F.data[:13] == 'search-place|')
async def process(callback: CallbackQuery, state: FSMContext):
    # await callback.message.delete()

    place = callback.data.split('|')[-1]
    hotels = await bot_db.get_place_hotels(place)
    if not hotels:
        await callback.answer(text='❌ Отелей не найдено!')
        return
    await bot_db.update_user_place(user_id=callback.from_user.id, place=place, arg='hotel')
    data = await bot_db.get_user_data(callback.from_user.id)
    date = data[7]
    count = data[8]
    place = data[10]
    children = data[9]
    await callback.message.edit_text(text=f'<b>❔ Вы хотите найти отель в поселке <i>{place}</i>, '
                                          f'на <i>{count} человек, дети: {children}, </i> '
                                          f'в период <i>{date}</i>?</b>\n\n'
                                          f'<i>Все верно?</i>',
                                     reply_markup=await get_confirm_data_kb())


@menu_router.callback_query(F.data == 'cancel-search')
async def process(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text='<b>✅ Введенные данные были удалены, заявка отменена.</b>\n\n'
                                          '<b>👋 Добро пожаловать в главное меню бота для подбора отеля.\n\n'
                                          'Тут вы можете выбрать отель для отдыха.</b>',
                                     reply_markup=await get_start_kb(callback.from_user.id))


@menu_router.callback_query(F.data[:12] == 'cancel-user|')
async def process(callback: CallbackQuery):
    await callback.message.edit_text(text='Заявка успешно отклонена!',
                                     reply_markup=await get_start_kb(callback.from_user.id))


@menu_router.callback_query(F.data[:10] == 'conf_user|')
async def process(callback: CallbackQuery):
    user_id = int(callback.data.split('|')[-2])
    hotel_rowid = int(callback.data.split('|')[-1])
    data = await bot_db.get_user_data(callback.from_user.id)
    user_date = data[7]
    user_count = data[8]
    user_children = data[9]
    user_place = data[10]
    hotel_data = await bot_db.get_hotel_data(user_id=callback.from_user.id, rowid=hotel_rowid)
    hotel_name, hotel_place, hotel_desc, hotel_contacts, hotel_photo = hotel_data[1:]
    media = [InputMediaPhoto(media=file_id) for file_id in hotel_photo.split('|')]
    await tgbot.send_media_group(chat_id=user_id,
                                 media=media)
    await tgbot.send_message(chat_id=user_id,
                             text='<b>✅ На вашу заявку откликнулся отель!</b>\n\n'
                                   f'Отель <i>"{hotel_name}"</i> в поселке <i>{hotel_place}</i> согласен вас заселить!\n'
                                   f'👤 Контакты отеля: <i>скрыты до оплаты</i>\n\n'
                                   f'<b>Вы указали:</b>\n'
                                   f'Время: <i>{user_date}</i>\n'
                                   f'Количество: <i>{user_count} человек</i>\n'
                                   f'Дети: <i>{user_children}</i>\n'
                                   f'Поселок: <i>{user_place}</i>\n\n'
                                   f'Если вас устраивает предложение, нажмите\n<b>"✅ Согласен"</b>\nесли нет -\n<b>"❌ Откажусь"</b>',
                           reply_markup=await get_confirm_hotel(callback.from_user.id, hotel_rowid))
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='✅ <b>Заявка успешно отправлена! Ожидайте решения пользователя.</b>',
                             reply_markup=await get_start_kb(callback.from_user.id))


@menu_router.callback_query(F.data[:16] == 'conf_user_banya|')
async def process(callback: CallbackQuery):
    user_id = int(callback.data.split('|')[-2])
    banya_rowid = int(callback.data.split('|')[-1])
    data = await bot_db.get_user_data(callback.from_user.id)
    user_date = data[27]
    user_time = data[28]
    user_count = data[29]
    user_place = data[30]
    banya_data = await bot_db.get_banya_data(user_id=callback.from_user.id, rowid=banya_rowid)
    name, place, desc, contacts, photo = banya_data[1:]
    await tgbot.send_photo(chat_id=callback.from_user.id,
                           caption='<b>✅ На вашу заявку откликнулась баня!</b>\n\n'
                                   f'Баня <i>"{name}"</i> в поселке <i>{place}</i> согласен вас заселить!\n'
                                   f'👤 Контакты отеля: <i>скрыты до оплаты</i>\n\n'
                                   f'<b>Вы указали:</b>\n'
                                   f'Время: <i>{user_date}</i>\n'
                                   f'Количество: <i>{user_count} человек</i>\n'
                                   f'Время: <i>{user_time}</i>\n'
                                   f'Поселок: <i>{user_place}</i>\n\n'
                                   f'Если вас устраивает предложение, нажмите\n<b>"✅ Согласен"</b>\nесли нет -\n<b>"❌ Откажусь"</b>',
                           reply_markup=await get_confirm_banya(callback.from_user.id, banya_rowid),
                           photo=photo)
    await tgbot.send_message(chat_id=user_id,
                             text='✅ <b>Заявка успешно принята! Ожидайте ответа пользователя.</b>',
                             reply_markup=await get_start_kb(callback.from_user.id))


@menu_router.callback_query(F.data[:16] == 'conf_user_trans|')
async def process(callback: CallbackQuery):
    user_id = int(callback.data.split('|')[-2])
    transfer_rowid = int(callback.data.split('|')[-1])
    user_data = await bot_db.get_user_data(callback.from_user.id)
    count = user_data[19]
    banya_data = await bot_db.get_transfer_data(user_id=callback.from_user.id, rowid=transfer_rowid)
    name, place, desc, contacts, photo = banya_data[1:]
    await tgbot.send_photo(chat_id=user_id,
                           caption='<b>✅ На вашу заявку откликнулся трансфер!</b>\n\n'
                                   f'Трансфер <i>{name}</i> согласен вас перевезти\n'
                                   f'👤 Контакты трансфера: <i><code>{contacts}</code></i>\n\n'
                                   f'<b>Вы указали:</b>\n'
                                   f'<i>{count}</i>\n\n'
                                   f'Если вас устраивает предложение, нажмите\n<b>"✅ Согласен"</b>\nесли нет -\n<b>"❌ Откажусь"</b>',
                           reply_markup=await get_confirm_transfer(callback.from_user.id, transfer_rowid),
                           photo=photo)
    await callback.message.edit_text(text='✅ <b>Заявка успешно принята! Ожидайте ответа пользователя.</b>',
                                     reply_markup=await get_start_kb(callback.from_user.id))



@menu_router.callback_query(F.data[:11] == 'conf-hotel|')
async def process(callback: CallbackQuery):
    await callback.message.delete()
    user_id = int(callback.data.split('|')[-2])
    hotel_rowid = int(callback.data.split('|')[-1])
    data = await bot_db.get_hotel_data(user_id, hotel_rowid)
    hotel_contacts = data[4]
    await tgbot.send_message(chat_id=user_id,
                             text='✅ <b>Пользователь согласился на заселение! Ожидайте, скоро с вами свяжутся</b>\n\n')
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='✅ <b>Вы согласились на предложение отеля. Свяжитесь с представителем отеля как можно быстрее!</b>\n\n'
                                  f'👤 Контакты отеля: <i>скрыты до оплаты</i>\n\n'
                                  f'Совершите')


@menu_router.callback_query(F.data[:13] == 'cancel-hotel|')
async def process(callback: CallbackQuery):
    await callback.message.delete()
    user_id = callback.data.split('|')[-1]
    await tgbot.send_message(chat_id=user_id,
                             text='❌ <b>Пользователь отказался от предложения.</b>\n\n')
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='✅ <b>Вы отказались от предложения.</b>\n\n')


@menu_router.callback_query(F.data[:11] == 'conf-banya|')
async def process(callback: CallbackQuery):
    await callback.message.delete()
    user_id = int(callback.data.split('|')[-2])
    banya_rowid = int(callback.data.split('|')[-1])
    data = await bot_db.get_banya_data(user_id, banya_rowid)
    banya_contacts = data[5]
    await tgbot.send_message(chat_id=user_id,
                             text='✅ <b>Пользователь согласился на предложение бани! Ожидайте, скоро с вами свяжутся</b>\n\n')
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='✅ <b>Вы согласились на предложение бани. Свяжитесь с ее представителем как можно быстрее!</b>\n\n'
                                   f'👤 Контакты бани: <i><code>{banya_contacts}</code></i>')


@menu_router.callback_query(F.data[:13] == 'cancel-banya|')
async def process(callback: CallbackQuery):
    await callback.message.delete()
    user_id = callback.data.split('|')[-1]
    await tgbot.send_message(chat_id=user_id,
                             text='❌ <b>Пользователь отказался от предложения.</b>\n\n')
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='✅ <b>Вы отказались от предложения.</b>\n\n')


@menu_router.callback_query(F.data[:11] == 'conf-trans|')
async def process(callback: CallbackQuery):
    await callback.message.delete()
    user_id = int(callback.data.split('|')[-2])
    transfer_rowid = int(callback.data.split('|')[-1])
    data = await bot_db.get_transfer_data(user_id, transfer_rowid)
    transfer_contacts = data[4]
    await tgbot.send_message(chat_id=user_id,
                             text='✅ <b>Пользователь согласился на предлоежние трансфера! Ожидайте, скоро с вами свяжутся</b>\n\n')
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='✅ <b>Вы согласились на предложение трансфера. Свяжитесь с представителем как можно быстрее!</b>\n\n'
                                   f'👤 Контакты компании: <i><code>{transfer_contacts}</code></i>')


@menu_router.callback_query(F.data[:13] == 'cancel-trans|')
async def process(callback: CallbackQuery):
    await callback.message.delete()
    user_id = callback.data.split('|')[-1]
    await tgbot.send_message(chat_id=user_id,
                             text='❌ <b>Пользователь отказался от предложения.</b>\n\n')
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text='✅ <b>Вы отказались от предложения.</b>\n\n')


@menu_router.callback_query(F.data == 'cancel-trans')
async def process(callback: CallbackQuery):
    await callback.message.edit_text(text='✅ <b>Заявка отменена!</b>')



@menu_router.callback_query(F.data == 'my-transfer')
async def process(callback: CallbackQuery):
    try:
        await callback.message.edit_text(text='Список ваших трансферных предложений:',
                                         reply_markup=await get_transfers_kb(callback.from_user.id))
    except:
        await callback.message.delete()
        await tgbot.send_message(chat_id=callback.from_user.id,
                                 text='Список ваших трансферных предложений:',
                                 reply_markup=await get_transfers_kb(callback.from_user.id))


@menu_router.callback_query(F.data == 'confirm-search')
async def process(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user_data = await bot_db.get_user_data(callback.from_user.id)
    place = user_data[5]
    date = user_data[7]
    count = user_data[8]
    place = user_data[10]
    children = user_data[9]
    print(user_data)
    hotels = await bot_db.get_place_hotels(place)
    user_ids = [i[0] for i in hotels]
    user_ids = set(user_ids)
    for user_id in user_ids:
        for hotel in hotels:
            if hotel[0] == user_id:
                await tgbot.send_message(chat_id=hotel[0],
                                         text=f'<b>📩 Пришел запрос от <a href="{callback.from_user.url}">клиента</a> {("(@" + callback.from_user.username + ")") or ""}</b>\n\n'  # {callback.from_user.full_name}
                                              f'На бронь отеля в <i>поселке {place}</i> в количестве <i>{count} человек, дети: {children}</i>, на период <i>{date}</i>',
                                         reply_markup=await get_confirm_request_hotel(user_id=callback.from_user.id,
                                                                                      owner_id=hotel[0]))
                break

    await callback.message.edit_text(text='<b>✅ Заявка на заселение отправлена владельцам.</b>\n\n'
                                          '<b>👋 Добро пожаловать в главное меню бота для подбора отеля.\n\n'
                                          'Тут вы можете выбрать отель для отдыха.</b>',
                                     reply_markup=await get_start_kb(callback.from_user.id))


@menu_router.callback_query(F.data == 'confirm-banya')
async def process(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user_data = await bot_db.get_user_data(callback.from_user.id)
    date = user_data[27]
    time = user_data[28]
    count = user_data[29]
    place = user_data[30]
    print(user_data)
    banyas = await bot_db.get_place_banyas(place)
    user_ids = [i[0] for i in banyas]
    user_ids = set(user_ids)
    for user_id in user_ids:
        for banya in banyas:
            if banya[0] == user_id:
                await tgbot.send_message(chat_id=banya[0],
                                         text=f'<b>📩 Пришел запрос от <a href="{callback.from_user.url}">клиента</a> {("(@" + callback.from_user.username + ")") or ""}</b>\n\n'  # {callback.from_user.full_name}
                                              f'На бронь бани в <i>поселке {place}</i> в количестве <i>{count} человек</i>, во время <i>{time}</i>, на период <i>{date}</i>',
                                         reply_markup=await get_confirm_request_banya(callback.from_user.id, banya[0]))
                break

    await callback.message.edit_text(text='<b>✅ Заявка на заселение отправлена владельцам.</b>\n\n'
                                          '<b>👋 Добро пожаловать в главное меню бота для подбора отеля.\n\n'
                                          'Тут вы можете выбрать отель для отдыха.</b>',
                                     reply_markup=await get_start_kb(callback.from_user.id))


@menu_router.callback_query(F.data == 'confirm-trans')
async def process(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user_data = await bot_db.get_user_data(callback.from_user.id)
    count = user_data[19]

    await callback.message.edit_text(text='<b>✅ Предложение отправлено, ожидайте отклика</b>')

    transfers = await bot_db.get_all_transfers()
    user_transfer = list()
    if not transfers:
        await callback.answer(text='❌ Трансферных предложений нет!')
    for transfer in transfers:
        if transfer[0] not in user_transfer:
            user_transfer.append(transfer[0])
            await tgbot.send_message(chat_id=transfer[0],
                                     text=f'<b>📩 Пришел запрос от <a href="{callback.from_user.url}">клиента</a> {("(@" + callback.from_user.username + ")") or ""}</b>\n'
                                          f'<i>Текст заявки:</i>\n\n' + count,
                                     reply_markup=await get_confirm_request_transfer(callback.from_user.id, transfer[0]))

    # user_data = await bot_db.get_user_data(callback.from_user.id)
    # place_from = user_data[21]
    # place_to = user_data[16]
    # count = user_data[19]
    # children = user_data[20]
    # date = user_data[17]
    # time = user_data[18]
    # transfers = await bot_db.get_place_transfers(place_from)
    # user_ids = [i[0] for i in transfers]
    # user_ids = set(user_ids)
    # for user_id in user_ids:
    #     for transfer in transfers:
    #         if transfer[0] == user_id:
    #             await tgbot.send_message(chat_id=transfer[0],
    #                                      text=f'<b>📩 Пришел запрос от <a href="{callback.from_user.url}">клиента</a> {("(@" + callback.from_user.username + ")") or ""}</b>\n\n'  # {callback.from_user.full_name}
    #                                           f'На трансфер из <i>поселка {place_from}</i> в <i>поселок {place_to} в </i>количестве <i>{count} человек, дети: {children}</i> во время <i>{time}</i>, на период <i>{date}</i>',
    #                                      reply_markup=await get_confirm_request_transfer(callback.from_user.id, transfer[0]))
    #             break

    await callback.message.edit_text(text='<b>✅ Заявка на трансфер отправлена</b>\n\n'
                                          '<b>👋 Добро пожаловать в главное меню бота для подбора отеля.\n\n'
                                          'Тут вы можете выбрать отель для отдыха.</b>',
                                     reply_markup=await get_start_kb(callback.from_user.id))



@menu_router.callback_query(F.data == 'my-hotels')
async def process(callback: CallbackQuery):
    try:
        await callback.message.edit_text(text='Список ваших отелей:',
                                         reply_markup=await get_hotels_kb(callback.from_user.id))
    except:
        await callback.message.delete()
        await tgbot.send_message(chat_id=callback.from_user.id,
                                 text='Список ваших отелей:',
                                 reply_markup=await get_hotels_kb(callback.from_user.id))


@menu_router.callback_query(F.data[:10] == 'my-hotels|')
async def process(callback: CallbackQuery):
    hotel_rowid = callback.data.split('|')[-1]
    hotel_data = await bot_db.get_hotel_data(user_id=callback.from_user.id, rowid=hotel_rowid)
    hotel_name, hotel_place, hotel_desc, hotel_contacts, hotel_photo = hotel_data[1:]
    await callback.message.delete()
    await tgbot.send_photo(chat_id=callback.from_user.id,
                           caption='<b>Ваш отель:</b>\n\n'
                                   f'Название: {hotel_name}\n'
                                   f'Поселок: {hotel_place}\n'
                                   f'Описание: {hotel_desc}\n'
                                   f'Контакты: {hotel_contacts}\n'
                                   'Фото: *сверху*',
                           reply_markup=await get_my_hotels_back_kb(hotel_name),
                           photo=hotel_photo)



@menu_router.callback_query(F.data[:10] == 'del-hotel|')
async def process(callback: CallbackQuery):
    hotel_name = callback.data.split('|')[-1]
    hotel_data = await bot_db.get_hotel_data(user_id=callback.from_user.id, name=hotel_name)
    print(hotel_data)
    hotel_data = await bot_db.get_hotel_data(user_id=callback.from_user.id, name=hotel_name)
    hotel_name, hotel_place, hotel_desc, hotel_contacts, hotel_photo = hotel_data[1:]
    await callback.message.delete()
    await tgbot.send_message(chat_id=callback.from_user.id,
                             text=f'Вы точно хотите удалить отель <i>{hotel_name}</i>?',
                             reply_markup=await get_del_hotel_confirm_kb(hotel_name))


@menu_router.callback_query(F.data[:18] == 'del-hotel-confirm|')
async def process(callback: CallbackQuery):
    hotel_name = callback.data.split('|')[-1]
    await bot_db.delete_hotel(user_id=callback.from_user.id, name=hotel_name)
    await callback.message.edit_text(text='Отель успешно удален!')


@menu_router.callback_query(F.data == 'my-banya')
async def process(callback: CallbackQuery):
    try:
        await callback.message.edit_text(text='Список ваших бань:',
                                         reply_markup=await get_banyas_kb(callback.from_user.id))
    except:
        await callback.message.delete()
        await tgbot.send_message(chat_id=callback.from_user.id,
                                 text='Список ваших бань:',
                                 reply_markup=await get_banyas_kb(callback.from_user.id))


@menu_router.callback_query(F.data[:4] == 'cal|')
async def process(callback: CallbackQuery):
    arg, offset = callback.data.split('|')[1:]
    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=await get_calendar_kb(arg=arg, offset=int(offset)))


@menu_router.callback_query(F.data[:15] == 'hotel-from-day|')
async def process(callback: CallbackQuery):
    date_from = callback.data.split('|')[-1]
    await bot_db.update_user_date(arg='hotel', user_id=callback.from_user.id, date=date_from)
    await callback.message.edit_text(text=callback.message.text + f'\n\n<i>С {date_from} по ...</i>',
                                     reply_markup=await get_calendar_kb(arg='hotel-to'))


@menu_router.callback_query(F.data[:13] == 'hotel-to-day|')
async def process(callback: CallbackQuery):
    date_to = callback.data.split('|')[-1]
    data = await bot_db.get_user_data(callback.from_user.id)
    date_from = data[7]
    await bot_db.update_user_date(arg='hotel', user_id=callback.from_user.id, date=f'{date_from} - {date_to}')
    await callback.message.edit_text(text=callback.message.text[:-3] + date_to,
                                     reply_markup=await get_confirm_date_keyboard('hotel'))


@menu_router.callback_query(F.data == 'confirm-date-hotel')
async def process(callback: CallbackQuery, state: FSMContext):
    prev_msg = await callback.message.edit_text(text='<b>✏ Введите количество человек</b>',
                                                reply_markup=await get_search_cancel_kb())

    await state.set_state(SearchState.search_count)
    await state.update_data(data={'prev_msg': prev_msg})


@menu_router.callback_query(F.data == 'cancel-date-hotel')
async def process(callback: CallbackQuery):
    await callback.message.edit_text(text='<b>✏ Выберите дату посещения</b>',
                                     reply_markup=await get_calendar_kb(arg='hotel-from'))


@menu_router.callback_query(F.data[:20] == 'transfer-from-place|')
async def process(callback: CallbackQuery):
    place = callback.data.split('|')[-1]
    await bot_db.update_user_place(arg='transfer', user_id=callback.from_user.id, place=place)
    await callback.message.edit_text(text='<b>✏ Выберите поселок, куда вы заказываете трансфер:</b>\n\n'
                                          f'<i>Из {callback.data.split("|")[-1]} в ...</i>',
                                     reply_markup=await get_places_kb(arg='transfer-to'))


@menu_router.callback_query(F.data[:18] == 'transfer-to-place|')
async def process(callback: CallbackQuery):
    place = callback.data.split('|')[-1]
    data = await bot_db.get_user_data(callback.from_user.id)
    place_from = data[21]
    await bot_db.update_user_to(arg='transfer', user_id=callback.from_user.id, to=place)
    await callback.message.edit_text(text='<b>✏ Выберите поселок, куда вы заказываете трансфер:</b>\n\n'
                                          f'<i>Из {place_from} в {place}</i>',
                                     reply_markup=await get_confirm_place_kb(arg='transfer'))



@menu_router.callback_query(F.data == 'cancel-place-transfer')
async def process(callback: CallbackQuery):
    await callback.message.edit_text(text='<b>✏ Выберите дату трансфера</b>',
                                     reply_markup=await get_calendar_kb(arg='transfer'))


@menu_router.callback_query(F.data == 'confirm-place-transfer')
async def process(callback: CallbackQuery, state: FSMContext):
    await bot_db.update_user_date(user_id=callback.from_user.id, date=callback.data.split('|')[-1], arg='transfer')
    prev_msg = await callback.message.edit_text(text='<b>✏ Введите время трансфера</b>',
                                                reply_markup=await get_search_cancel_kb())
    await state.set_state(SearchState.transfer_time)
    await state.update_data(data={'prev_msg': prev_msg})


@menu_router.callback_query(F.data[:11] == 'all-hotels|')
async def process(callback: CallbackQuery):
    offset = int(callback.data.split('|')[-1])
    await callback.message.edit_text(text='Все отели',
                                     reply_markup=await get_all_hotels_kb(offset))


@menu_router.callback_query(F.data[:11] == 'all-places|')
async def process(callback: CallbackQuery):
    offset = int(callback.data.split('|')[-1])
    await callback.message.edit_text(text='Все поселки',
                                     reply_markup=await get_all_places_kb(offset))


@menu_router.callback_query(F.data[:10] == 'all-trans|')
async def process(callback: CallbackQuery):
    offset = int(callback.data.split('|')[-1])
    await callback.message.edit_text(text='Все трансферы',
                                     reply_markup=await get_all_transfers_kb(offset))


@menu_router.callback_query(F.data[:10] == 'all-users|')
async def process(callback: CallbackQuery):
    offset = int(callback.data.split('|')[-1])
    await callback.message.edit_text(text='Все пользователи',
                                     reply_markup=await get_all_users_kb(offset))


@menu_router.callback_query(F.data[:15] == 'all-hotels-adm|')
async def process(callback: CallbackQuery):
    user_id, name = callback.data.split('|')
    user_data = await bot_db.get_user_data(int(user_id))
    hotel_data = await bot_db.get_hotel_data(int(user_id), name)
    name, place, desc, contacts, photo = hotel_data[1:]
    await callback.message.delete()
    await tgbot.send_photo(caption=f'<b>Отель пользователя <a href="tg://user?id={user_id}">{user_data[-1]}</a>:</b>\n\n'
                                   f'Название: {name}\n'
                                   f'Поселок: {place}\n'
                                   f'Описание: {desc}\n'
                                   f'Контакты: {contacts}\n',
                           photo=photo,
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='all-hotels|0')]]))


@menu_router.callback_query(F.data[:15] == 'all-places-adm|')
async def process(callback: CallbackQuery):
    name = callback.data.split('|')[-1]
    await callback.message.edit_text(text=f'<b>Поселок {name}</b>',
                                     reply_markup=InlineKeyboardMarkup(
                                         inline_keyboard=[
                                             [InlineKeyboardButton(text='Назад', callback_data='all-places|0'),
                                              InlineKeyboardButton(text='Удалить', callback_data=f'del-place|{name}')]]))


@menu_router.callback_query(F.data[:14] == 'all-trans-adm|')
async def process(callback: CallbackQuery):
    user_id, name = callback.data.split('|')
    user_data = await bot_db.get_user_data(int(user_id))
    transfer_data = await bot_db.get_transfer_data(int(user_id), name)
    name, place, desc, contacts, photo = transfer_data[1:]
    await callback.message.delete()
    await tgbot.send_photo(caption=f'<b>Трансфер пользователя <a href="tg://user?id={user_id}">{user_data[-1]}</a>:</b>\n\n'
                                   f'Название: {name}\n'
                                   f'Поселок: {place}\n'
                                   f'Описание: {desc}\n'
                                   f'Контакты: {contacts}\n',
                           photo=photo,
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='all-trans|0')]]))


@menu_router.callback_query(F.data[:14] == 'all-users-adm|')
async def process(callback: CallbackQuery):
    user_id = callback.data.split('|')[-1]
    user_data = await bot_db.get_user_data(int(user_id))
    await callback.message.edit_text(text=f'<b>Пользователь <a href="tg://user?id={user_id}">{user_data[-1]}</a>:</b>\n\n'
                                          f'Статус: {user_data[1]}',
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='all-users|0')]]))


@menu_router.callback_query(F.data[:10] == 'del-place|')
async def process(callback: CallbackQuery):
    name = callback.data.split('|')[-1]
    await bot_db.del_place(name)
    await callback.message.edit_text(text=f'<b>Поселок <i>{name}</i> удален успешно!</b>')