from aiogram import F
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link

from bot.main_loader import tgbot

from bot.handlers.callback.callback_states import SearchState
from bot.handlers.callback.callback_kb import *
from mangaparser.manga_parser import manga_parser

from database.bot_database import bot_db
from database.manga_database import manga_db

from telegraphposter.telegraph_poster import telegraph_poster

state_router = Router()


@state_router.message(SearchState.search_request)
async def process_search(msg: Message, state: FSMContext):
    await state.clear()
    await msg.delete()
    search_request = msg.text
    message = await bot_db.get_user_message(user_id=msg.from_user.id)
    print(message)
    await tgbot.edit_message_text(chat_id=msg.from_user.id,
                                  message_id=message,
                                  text=f'<b>Запрос</b>: {search_request}\n\n'
                                       f'<i>Поиск...</i>')
    search_result = await manga_parser.search(search_request)
    print(search_result)

    await tgbot.edit_message_text(chat_id=msg.from_user.id,
                                  message_id=message,
                                  text=f'<b>Результаты писка по запросу: {search_request}</b>')
    manga_messages = list()
    search_paths = list()
    cover_urls = list()
    for n, i in enumerate(search_result):
        photo_message = await tgbot.send_message(chat_id=msg.from_user.id,
                                                 text=f'{hide_link(i[3])}'
                                                      f'Название: <b>{i[0]}</b>\n'
                                                      f'Альтернативное название: <b>{i[2]}</b>',
                                                 reply_markup=await get_search_manga_kb(n)
                                                 )
        search_paths.append(i[1])
        manga_messages.append(photo_message.message_id)
        cover_urls.append(i[3])
    print(search_paths)
    await state.set_state(SearchState.manga_info)
    # await state.update_data(manga_messages=manga_messages)
    # await state.update_data(search=search_paths)
    await state.update_data({'manga_messages': manga_messages,
                             'search': search_paths,
                             'cover': cover_urls})


@state_router.message(SearchState.goto)
async def process_goto(msg: Message, state: FSMContext):
    await msg.delete()
    await state.set_state(SearchState.manga_info)
    data = await state.get_data()
    vols = data['vols']
    user_msg = await bot_db.get_user_message(user_id=msg.from_user.id)
    if msg.text.isdigit():
        num = int(msg.text)
        if num > len(vols):
            num = len(vols)
        url = vols[-num]
        title = url[1]
        source = url[0]
        if not await manga_db.is_manga_exists(title=url[1]):
            await tgbot.edit_message_text(chat_id=msg.from_user.id,
                                          message_id=user_msg,
                                          text='⏳ <b>Загрузка страниц манги...</b>')
            manga = await manga_parser.get_manga(url[0])
            telegraph_url = await telegraph_poster.upload_page(source_url=source, title_start=url, title_end=title,
                                                               content_list=manga)
        else:
            info = await manga_db.get_manga_info(title)
            telegraph_url = info['telegraph_url']
        await tgbot.edit_message_text(chat_id=msg.from_user.id,
                                      message_id=user_msg,
                                      text=f'{hide_link(telegraph_url)}'
                                           f'{title}',
                                      reply_markup=await get_read_manga_kb(path=num + 1,
                                                                           title={'next': vols[-num - 1][1],
                                                                                  'prev': vols[-num + 1][1]} if (num + 1) <= len(vols) else
                                                                                 {'prev': vols[-num + 1][1]},
                                                                           len_vols=len(vols)))
    else:
        await tgbot.edit_message_text(chat_id=msg.from_user.id,
                                      message_id=user_msg,
                                      text=f'{hide_link(data["cover"])}'
                                           f'<i>{data["title"]}</i>\n\n'
                                           f'❗ <b>Ошибка! Неверный формат данных\n'
                                           f'🔎 Необходимый формат данных: натуральное число (1, 2, 3 и т.д.)</b>',
                                      reply_markup=await get_read_manga_kb(path=1,
                                                                           title={'next': data['title']},
                                                                           len_vols=len(vols)))