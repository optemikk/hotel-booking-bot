from aiogram import types
from aiogram.filters import Command
from bot.main_loader import tgbot

import asyncio
from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Any, Awaitable, Union

from bot.menu.states.states_kb import get_places_kb
from bot.start.commands.command_kb import get_start_kb

from bot.add_hotel.loader import add_hotel_router
from bot.add_hotel.commands.command_kb import get_places_kb, get_allow_posting_kb
from aiogram.types.input_file import InputFile
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.types import Message, InputMediaPhoto, InputMedia, ContentType as CT
from aiogram import F

from database.bot_database import bot_db


class AlbumMiddleware(BaseMiddleware):
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        self.latency = latency

    async def __call__(
            self,
            handler: Callable[[Message, dict], Awaitable[Any]],
            message: Message,
            data: dict
    ) -> Any:
        if not message.media_group_id:
            await handler(message, data)
            return
        try:
            self.album_data[message.media_group_id].append(message)
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            data['_is_last'] = True
            data["album"] = self.album_data[message.media_group_id]
            await handler(message, data)

        if message.media_group_id and data.get("_is_last"):
            del self.album_data[message.media_group_id]
            del data['_is_last']


@add_hotel_router.message(Command('add'))
async def process(msg: types.Message):
    await msg.delete()
    status = await bot_db.get_user_status(msg.from_user.id)
    print(status)
    if status != 'howner':
        await msg.answer(text='<b>❌ Ваш статус не позволяет вам добавлять отели! '
                              'Подождите, пока вашу заявку одобрят.</b>\n\n')
        await tgbot.send_message(chat_id=972383332,
                                 text='<b>Поступил запрос на одобрение статуса пользователя!</b>\n\n'
                                      f'Пользователь <i><a href="{msg.from_user.url}">{msg.from_user.username or msg.from_user.full_name}</a></i> '
                                      f'просит разрешение на публикацию своих услуг.\n\nРазрешить?',
                                 reply_markup=await get_allow_posting_kb(msg.from_user.id))
    else:
        await msg.answer(text='<b>✏ Выберите поселок для вашего отеля.</b>',
                         reply_markup=await get_places_kb())

    # -> bot.menu.callback.callback_handler