from aiogram import types
from aiogram.filters import Command
from bot.start.commands.command_kb import get_start_kb

from database.bot_database import bot_db
from bot.add_place.loader import add_place_router


@add_place_router.message(Command('add_place'))
async def process(msg: types.Message):
    await msg.delete()
    await bot_db.add_place(name=' '.join(msg.text.split(' ')[1:]))


@add_place_router.message(Command('places'))
async def process(msg: types.Message):
    await msg.delete()
    places = await bot_db.get_all_places()
    await msg.answer(text='Все поселки:\n' + '\n'.join([place[0] for place in places]))


@add_place_router.message(Command('hotels'))
async def process(msg: types.Message):
    await msg.delete()
    user_data = await bot_db.get_user_data(msg.from_user.id)
    place = user_data[4]
    hotels = await bot_db.get_place_hotels(place)
    print(user_data)
    print(hotels)
    print(msg.from_user.url)
    # for hotel in hotels:
    #     print(hotel[0])
