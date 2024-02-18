from bot.main_loader import tgbot
from aiogram import Router
from aiogram.types import Message

from bot.text.loader import text_router

echo_router = Router()


@echo_router.message()
async def echo(msg: Message):
    message_id = msg.message_id
    message = await tgbot.copy_message(message_id=message_id, from_chat_id=msg.from_user.id, chat_id=msg.from_user.id)

    # await msg.answer(text=str(msg.text.isdigit()))