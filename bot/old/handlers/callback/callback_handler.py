import aiogram
from aiogram import types
from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link
from aiogram import F

from bot.main_loader import tgbot

from mangaparser import manga_parser
from telegraphposter import telegraph_poster

from bot.handlers.callback.callback_kb import *
from bot.handlers.callback.callback_text import *
from bot.handlers.callback.callback_states import SearchState
from bot.handlers.commands.command_kb import *
# from bot.handlers.callback.callback_filters import *

from database.bot_database import bot_db
from database.manga_database import manga_db


callback_router = Router()


@callback_router.callback_query(F.data == 'search')
async def search(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchState.search_request)
    await callback.message.edit_text(text='✏ Введите название манги, которую хотите прочесть...')


@callback_router.callback_query(F.data[:4] == 'open', SearchState.manga_info)
async def open_manga(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    for i in data['manga_messages']:
        await tgbot.delete_message(chat_id=callback.from_user.id,
                                   message_id=i)
    user_main_message = await bot_db.get_user_message(user_id=callback.from_user.id)
    await tgbot.edit_message_text(chat_id=callback.from_user.id,
                                  message_id=user_main_message,
                                  text='<b>Загрузка, ожидайте...</b>')
    search_urls = data['search']
    num = callback.data.split('|')[1]
    url = search_urls[int(num)]
    cover_url = data['cover'][int(num)]
    html = await manga_parser.open_page(url)
    vols = await manga_parser.get_vols(html)
    vols = vols['vols']
    title = vols[-1][1]

    await tgbot.edit_message_text(chat_id=callback.from_user.id,
                                  message_id=user_main_message,
                                  text=f'{hide_link(cover_url)}'
                                       f'<i>{title}</i>\n\n'
                                       f'<i>Глав всего</i>: <b>{len(vols)}</b>',
                                  reply_markup=await get_read_manga_kb(path=1,
                                                                       title={'next': title},
                                                                       len_vols=len(vols)))
    await state.update_data(vols=vols, source=url, title=title, cover=cover_url)
    await state.set_state(SearchState.manga_info)


@callback_router.callback_query(F.data[:3] == 'vol', SearchState.manga_info)
async def read_manga(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # source = data['source']
    # title = data['title']
    vols = data['vols']
    num = int(callback.data.split('|')[1])
    url = vols[-num]
    title = url[1]
    source = url[0]
    if not await manga_db.is_manga_exists(title=url[1]):
        await callback.message.edit_text(text='⏳ <b>Загрузка страниц манги...</b>')
        manga = await manga_parser.get_manga(url[0])
        telegraph_url = await telegraph_poster.upload_page(source_url=source, title_start=url, title_end=title, content_list=manga)
    else:
        info = await manga_db.get_manga_info(title)
        telegraph_url = info['telegraph_url']
    await tgbot.edit_message_text(chat_id=callback.from_user.id,
                                  message_id=await bot_db.get_user_message(user_id=callback.from_user.id),
                                  text=f'{hide_link(telegraph_url)}'
                                       f'{title}',
                                  reply_markup=await get_read_manga_kb(path=num + 1,
                                                                       title={'next': vols[-num - 1][1],
                                                                              'prev': vols[-num + 1][1]} if (num + 1) <= len(vols) else
                                                                             {'prev': vols[-num + 1][1]},
                                                                       len_vols=len(vols)))


@callback_router.callback_query(F.data == 'main')
async def return_to_main(callback: CallbackQuery):
    await callback.message.edit_text(text='🧾 Главное меню',
                                     reply_markup=await start_kb())


@callback_router.callback_query(F.data == 'goto')
async def go_to(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchState.goto)
    await callback.message.edit_text(text='➡️ <b>Введите номер главы, которую хотите открыть</b>')