import aiogram
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link
from bot.menu.loader import menu_router

from bot.main_loader import tgbot
from database.bot_database import bot_db

from bot.menu.states.states import SearchState
from bot.menu.states.states_kb import get_places_kb, get_confirm_transfer_kb
from bot.menu.callback.callback_kb import get_search_cancel_kb
from bot.start.commands.command_kb import get_start_kb


# <- bot.menu.callback.callback_handler

@menu_router.message(SearchState.transfer_data)
async def process(msg: Message, state: FSMContext):
    await msg.delete()

    data = await state.get_data()
    prev_msg: Message = data['prev_msg']

    await bot_db.update_user_count(user_id=msg.from_user.id,
                                   count=msg.text,
                                   arg='transfer')
    await prev_msg.edit_text(text='<b>❔ Ваша заявка:\n\n</b>' + msg.text + '\n\n<i>Все верно?</i>',
                             reply_markup=await get_confirm_transfer_kb())
    await state.clear()





@menu_router.message(SearchState.search_date)
async def process(msg: Message, state: FSMContext):
    await msg.delete()

    data = await state.get_data()
    prev_msg: Message = data['prev_msg']

    await bot_db.update_user_date(user_id=msg.from_user.id, date=msg.text, arg='hotel')

    await state.clear()
    prev_msg = await prev_msg.edit_text(text='<b>✏ Введите количество взрослых</b>',
                                        reply_markup=await get_search_cancel_kb())

    await state.set_state(SearchState.search_count)
    await state.update_data(data={'prev_msg': prev_msg})


@menu_router.message(SearchState.search_count)
async def process(msg: Message, state: FSMContext):
    await msg.delete()

    data = await state.get_data()
    prev_msg: Message = data['prev_msg']

    await bot_db.update_user_count(user_id=msg.from_user.id, count=msg.text, arg='hotel')

    await state.clear()
    prev_msg = await prev_msg.edit_text(text='<b>✏ Введите количество и возраст детей (если есть, иначе ответьте "нету")</b>',
                                        reply_markup=await get_search_cancel_kb())

    await state.set_state(SearchState.search_children)
    await state.update_data(data={'prev_msg': prev_msg})


@menu_router.message(SearchState.search_children)
async def process(msg: Message, state: FSMContext):
    await msg.delete()

    data = await state.get_data()
    prev_msg: Message = data['prev_msg']

    await bot_db.update_user_children(user_id=msg.from_user.id, children=msg.text, arg='hotel')

    await state.clear()
    await prev_msg.edit_text(text='<b>✏ Выберите поселок</b>',
                             reply_markup=await get_places_kb())

    # await state.update_data(data={'prev_msg': prev_msg})


@menu_router.message(SearchState.banya_date)
async def process(msg: Message, state: FSMContext):
    await msg.delete()

    data = await state.get_data()
    prev_msg: Message = data['prev_msg']

    await bot_db.update_user_date(user_id=msg.from_user.id, date=msg.text, arg='banya')
    prev_msg = await prev_msg.edit_text(text='<b>✏ Введите время посещения</b>',
                                        reply_markup=await get_search_cancel_kb())

    await state.set_state(SearchState.banya_time)
    await state.update_data(data={'prev_msg': prev_msg})


@menu_router.message(SearchState.banya_time)
async def process(msg: Message, state: FSMContext):
    await msg.delete()

    data = await state.get_data()
    prev_msg: Message = data['prev_msg']

    await bot_db.update_user_time(user_id=msg.from_user.id, time=msg.text, arg='banya')
    prev_msg = await prev_msg.edit_text(text='<b>✏ Введите количество взрослых</b>',
                                        reply_markup=await get_search_cancel_kb())

    await state.set_state(SearchState.banya_count)
    await state.update_data(data={'prev_msg': prev_msg})


@menu_router.message(SearchState.banya_count)
async def process(msg: Message, state: FSMContext):
    await msg.delete()

    data = await state.get_data()
    prev_msg: Message = data['prev_msg']
    await prev_msg.edit_text(text='<b>✏ Выберите поселок с баней</b>',
                             reply_markup=await get_places_kb(arg='banya'))

    await state.clear()


@menu_router.message(SearchState.transfer_time)
async def process(msg: Message, state: FSMContext):
    await msg.delete()

    data = await state.get_data()
    prev_msg: Message = data['prev_msg']
    await prev_msg.edit_text(text='<b>✏ Введите количество взрослых</b>',
                             reply_markup=await get_search_cancel_kb())

    await state.set_state(SearchState.transfer_count)
    await state.update_data(data={'prev_msg': prev_msg})


@menu_router.message(SearchState.transfer_count)
async def process(msg: Message, state: FSMContext):
    await msg.delete()

    data = await state.get_data()
    prev_msg: Message = data['prev_msg']
    await prev_msg.edit_text(text='<b>✏ Введите количество и возраст детей (если есть, иначе ответьте "нету")</b>',
                             reply_markup=await get_search_cancel_kb())

    await state.set_state(SearchState.transfer_children)
    await state.update_data(data={'prev_msg': prev_msg})


@menu_router.message(SearchState.transfer_children)
async def process(msg: Message, state: FSMContext):
    await msg.delete()

    data = await state.get_data()
    prev_msg: Message = data['prev_msg']
    user_data = await bot_db.get_user_data(msg.from_user.id)
    place_from = user_data[21]
    place_to = user_data[16]
    count = user_data[19]
    children = user_data[20]
    date = user_data[17]
    time = user_data[18]

    await prev_msg.edit_text(text=f'<b>❔ Вы хотите заказать трансфер из <i>{place_from}</i>, в <i>{place_to}</i>'
                                  f'на <i>{count} человек, дети: {children}, </i> '
                                  f'в период <i>{date}</i>, во время <i>{time}</i>?</b>\n\n'
                                  f'<i>Все верно?</i>',
                             reply_markup=await get_confirm_transfer_kb())