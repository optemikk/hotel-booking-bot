from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.bot_database import bot_db



async def get_confirm_date_keyboard(arg: str):
    keyboard = [
        [InlineKeyboardButton(text='Верно', callback_data=f'confirm-date-{arg}'),
         InlineKeyboardButton(text='Неверно', callback_data=f'cancel-date-{arg}')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_search_cancel_kb():
    keyboard = [
        [InlineKeyboardButton(text='❌ Отменить', callback_data='cancel-search')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_confirm_data_kb():
    keyboard = [
        [InlineKeyboardButton(text='✅ Подтвердить', callback_data='confirm-search'),
         InlineKeyboardButton(text='❌ Отменить', callback_data='cancel-search')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_confirm_request_hotel(user_id: int, owner_id: int):
    keyboard = [
        [InlineKeyboardButton(text='❌ Отменить', callback_data=f'cancel-user|{user_id}')]
    ]
    hotels = await bot_db.get_user_hotels(owner_id)
    [keyboard.append([InlineKeyboardButton(text='Отклик. ' + hotel[2], callback_data=f'conf_user|{user_id}|{hotel[0]}')]) for hotel in hotels]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_confirm_request_banya(user_id: int, owner_id: int):
    keyboard = [
        [InlineKeyboardButton(text='❌ Отменить', callback_data=f'cancel-user|{user_id}')]
    ]
    banyas = await bot_db.get_user_banyas(owner_id)
    [keyboard.append([InlineKeyboardButton(text='Отклик. ' + banya[2], callback_data=f'conf_user_banya|{banya[1]}|{banya[0]}')]) for banya in banyas]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_confirm_request_transfer(user_id: int, owner_id: int):
    keyboard = [
        [InlineKeyboardButton(text='❌ Отменить', callback_data=f'cancel-user|{user_id}')]
    ]
    transfers = await bot_db.get_user_transfers(owner_id)
    [keyboard.append([InlineKeyboardButton(text='Отклик. ' + transfer[2], callback_data=f'conf_user_trans|{transfer[1]}|{transfer[0]}')]) for transfer in transfers]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_confirm_hotel(user_id: int, rowid: str):
    keyboard = [
        [InlineKeyboardButton(text='✅ Согласен', callback_data=f'conf-hotel|{user_id}|{rowid}'),
         InlineKeyboardButton(text='❌ Откажусь', callback_data=f'cancel-hotel|{user_id}')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_confirm_banya(user_id: int, rowid: str):
    keyboard = [
        [InlineKeyboardButton(text='✅ Согласен', callback_data=f'conf-banya|{user_id}|{rowid}'),
         InlineKeyboardButton(text='❌ Откажусь', callback_data=f'cancel-banya|{user_id}')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_confirm_transfer(user_id: int, rowid: str):
    keyboard = [
        [InlineKeyboardButton(text='✅ Согласен', callback_data=f'conf-trans|{user_id}|{rowid}'),
         InlineKeyboardButton(text='❌ Откажусь', callback_data=f'cancel-trans|{user_id}')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_hotels_kb(user_id: int):
    user_hotels = await bot_db.get_user_hotels(user_id)
    keyboard = list()
    print(user_hotels)
    if user_hotels:
        [keyboard.append([InlineKeyboardButton(text=hotel[2], callback_data=f'my-hotels|{hotel[0]}')]) for hotel in user_hotels]
    keyboard.append([InlineKeyboardButton(text='❌ Назад', callback_data='start'), InlineKeyboardButton(text='✅ Добавить', callback_data='add-hotel')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_banya_cancel_kb():
    keyboard = [
        [InlineKeyboardButton(text='❌ Отменить', callback_data='cancel-banya')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_my_hotels_back_kb(hotel: str):
    keyboard = [
        [InlineKeyboardButton(text='❌ Назад', callback_data='my-hotels')],
        [InlineKeyboardButton(text='❌ Удалить отель', callback_data=f'del-hotel|{hotel}')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_del_hotel_confirm_kb(hotel: str):
    keyboard = [
        [InlineKeyboardButton(text='✅ Подтвердить', callback_data=f'del-hotel-confirm|{hotel}')],
        [InlineKeyboardButton(text='❌ Отказаться', callback_data=f'del-hotel-cancel')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_confirm_banya_search_kb():
    keyboard = [
        [InlineKeyboardButton(text='✅ Подтвердить', callback_data='confirm-banya'),
         InlineKeyboardButton(text='❌ Отменить', callback_data='cancel-search')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_banyas_kb(user_id: int):
    user_banyas = await bot_db.get_user_banyas(user_id)
    keyboard = list()
    if user_banyas:
        [keyboard.append([InlineKeyboardButton(text=banya[2], callback_data=f'my-banyas|{banya[2]}')]) for banya in user_banyas]
    keyboard.append([InlineKeyboardButton(text='❌ Назад', callback_data='start'), InlineKeyboardButton(text='✅ Добавить', callback_data='add-banya')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_transfers_kb(user_id: int):
    user_transfers = await bot_db.get_user_transfers(user_id)
    keyboard = list()
    if user_transfers:
        [keyboard.append([InlineKeyboardButton(text=transfer[1], callback_data=f'my-transf|{transfer[0]}')]) for transfer in
         user_transfers]
    keyboard.append([InlineKeyboardButton(text='❌ Назад', callback_data='start'),
                     InlineKeyboardButton(text='✅ Добавить', callback_data='add-transfer')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_confirm_place_kb(arg):
    keyboard = [
        [InlineKeyboardButton(text='Верно', callback_data=f'confirm-place-{arg}'),
         InlineKeyboardButton(text='Неверно', callback_data=f'transfer')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_all_hotels_kb(offset: int = 0):
    keyboard = list()
    hotels = await bot_db.get_all_hotels()
    if len(hotels) >= (offset + 1) * 5:
        hotels_slice = hotels[offset * 5:(offset + 1) * 5]
    else:
        hotels_slice = hotels[offset * 5:]

    for hotel in hotels_slice:
        keyboard.append([InlineKeyboardButton(text=hotel[1], callback_data=f'all-hotels-adm|{hotel[0]}|{hotel[1]}')])
    keyboard.append(
        [InlineKeyboardButton(text='<-', callback_data=f'all-hotels|{offset - 1}') if offset > 0 else
            InlineKeyboardButton(text='ㅤ', callback_data='none'),
         InlineKeyboardButton(text='.', callback_data='dot'),
         InlineKeyboardButton(text='->', callback_data=f'all-hotels|{offset + 1}') if len(hotels_slice) == 5 else
         InlineKeyboardButton(text='ㅤ', callback_data='none')] if len(hotels) > 5 else
        [InlineKeyboardButton(text='❌ Назад', callback_data='start')]
    )
    if len(hotels) > 5:
        keyboard.append([InlineKeyboardButton(text='❌ Назад', callback_data='start')])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_all_places_kb(offset: int = 0):
    keyboard = list()
    places = await bot_db.get_all_places()
    if len(places) >= (offset + 1) * 5:
        places_slice = places[offset * 5:(offset + 1) * 5]
    else:
        places_slice = places[offset * 5:]

    for place in places_slice:
        keyboard.append([InlineKeyboardButton(text=place[0], callback_data=f'all-places-adm|{place[0]}')])
    keyboard.append(
        [InlineKeyboardButton(text='<-', callback_data=f'all-places|{offset - 1}') if offset > 0 else
            InlineKeyboardButton(text='ㅤ', callback_data='none'),
         InlineKeyboardButton(text='.', callback_data='dot'),
         InlineKeyboardButton(text='->', callback_data=f'all-places|{offset + 1}') if len(places_slice) == 5 else
         InlineKeyboardButton(text='ㅤ', callback_data='none')] if len(places) > 5 else
        [InlineKeyboardButton(text='❌ Назад', callback_data='start'),
         InlineKeyboardButton(text='Добавить поселок', callback_data='add-place')]
    )
    if len(places) > 5:
        keyboard.append([InlineKeyboardButton(text='❌ Назад', callback_data='start'),
                         InlineKeyboardButton(text='Добавить поселок', callback_data='add-place')])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_all_transfers_kb(offset: int = 0):
    keyboard = list()
    transfers = await bot_db.get_all_transfers()
    if len(transfers) >= (offset + 1) * 5:
        transfers_slice = transfers[offset * 5:(offset + 1) * 5]
    else:
        transfers_slice = transfers[offset * 5:]

    for transfer in transfers_slice:
        keyboard.append([InlineKeyboardButton(text=transfer[1], callback_data=f'all-trans-adm|{transfer[1]}')])
    keyboard.append(
        [InlineKeyboardButton(text='<-', callback_data=f'all-trans|{offset - 1}') if offset > 0 else
            InlineKeyboardButton(text='ㅤ', callback_data='none'),
         InlineKeyboardButton(text='.', callback_data='dot'),
         InlineKeyboardButton(text='->', callback_data=f'all-trans|{offset + 1}') if len(transfers_slice) == 5 else
         InlineKeyboardButton(text='ㅤ', callback_data='none')] if len(transfers) > 5 else
        [InlineKeyboardButton(text='❌ Назад', callback_data='start')]
    )
    if len(transfers) > 5:
        keyboard.append([InlineKeyboardButton(text='❌ Назад', callback_data='start')])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_all_users_kb(offset: int = 0):
    keyboard = list()
    users = await bot_db.get_all_users()
    if len(users) >= (offset + 1) * 5:
        users_slice = users[offset * 5:(offset + 1) * 5]
    else:
        users_slice = users[offset * 5:]

    for user in users_slice:
        keyboard.append([InlineKeyboardButton(text=user[-1], callback_data=f'all-users-adm|{user[0]}')])
    keyboard.append(
        [InlineKeyboardButton(text='<-', callback_data=f'all-users|{offset - 1}') if offset > 0 else
            InlineKeyboardButton(text='ㅤ', callback_data='none'),
         InlineKeyboardButton(text='.', callback_data='dot'),
         InlineKeyboardButton(text='->', callback_data=f'all-users|{offset + 1}') if len(users_slice) == 5 else
         InlineKeyboardButton(text='ㅤ', callback_data='none')] if len(users) > 5 else
        [InlineKeyboardButton(text='❌ Назад', callback_data='start')]
    )
    if len(users) > 5:
        keyboard.append([InlineKeyboardButton(text='❌ Назад', callback_data='start')])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)