from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_search_manga_kb(num: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Открыть', callback_data=f'open|{num}')]
    ])
    return keyboard


async def get_read_manga_kb(path: int, title: dict, len_vols: int):
    # keyboard = InlineKeyboardMarkup(inline_keyboard=[
    #     [InlineKeyboardButton(text='📖' + title['next'], callback_data=f'vol|{path}')],
    #     [InlineKeyboardButton(text='➡️ Перейти на главу...', callback_data='goto')],
    #     [InlineKeyboardButton(text='⬅ Вернуться назад', callback_data='main')]
    # ] if path < 3 else [
    #     [InlineKeyboardButton(text='📖' + title['prev'], callback_data=f'vol|{path - 2}'),
    #      InlineKeyboardButton(text='📖' + title['next'], callback_data=f'vol|{path}')],
    #     [InlineKeyboardButton(text='➡️ Перейти на главу...', callback_data='goto')],
    #     [InlineKeyboardButton(text='⬅ Вернуться назад', callback_data='main')]
    # ])
    if path < 3:
        keyboard = [
            [InlineKeyboardButton(text='📖' + title['next'], callback_data=f'vol|{path}')],
            [InlineKeyboardButton(text='➡️ Перейти на главу...', callback_data='goto')],
            [InlineKeyboardButton(text='⬅ Вернуться назад', callback_data='main')]
        ]
    elif len_vols >= path >= 3:
        keyboard = [
            [InlineKeyboardButton(text='📖' + title['prev'], callback_data=f'vol|{path - 2}'),
             InlineKeyboardButton(text='📖' + title['next'], callback_data=f'vol|{path}')],
            [InlineKeyboardButton(text='➡️ Перейти на главу...', callback_data='goto')],
            [InlineKeyboardButton(text='⬅ Вернуться назад', callback_data='main')]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton(text='📖' + title['prev'], callback_data=f'vol|{path - 2}')],
            [InlineKeyboardButton(text='➡️ Перейти на главу...', callback_data='goto')],
            [InlineKeyboardButton(text='⬅ Вернуться назад', callback_data='main')]
        ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)