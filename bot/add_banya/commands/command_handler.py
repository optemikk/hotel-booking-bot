from aiogram import types
from aiogram.filters import Command
from bot.main_loader import tgbot

from bot.menu.states.states_kb import get_places_kb
from bot.start.commands.command_kb import get_start_kb

from bot.add_banya.loader import add_banya_router
from bot.add_banya.commands.command_kb import get_places_kb, get_allow_posting_kb

from database.bot_database import bot_db


@add_banya_router.message(Command('------'))
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