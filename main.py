# -*- coding: utf-8 -*-
import asyncio
import platform
from bot.main_loader import dp, tgbot

from bot.menu.callback.callback_handler import *
from bot.menu.states.state_handler import *

from bot.start.commands.command_handler import *

from bot.add_place.commands.command_handler import *
from bot.add_place.states.state_handler import *
from bot.add_place.callback.callback_handler import *

from bot.add_hotel.commands.command_handler import *
from bot.add_hotel.callback.callback_handler import *
from bot.add_hotel.states.state_handler import *

from bot.add_banya.states.state_handler import *
from bot.add_banya.callback.callback_handler import *

from bot.add_transfer.states.state_handler import *
from bot.add_transfer.callback.callback_handler import *

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main() -> None:
    dp.message.middleware(AlbumMiddleware())
    # dp.include_routers(echo_router)
    dp.include_routers(start_router)
    dp.include_routers(menu_router)
    dp.include_routers(add_place_router)
    dp.include_routers(add_hotel_router)
    dp.include_routers(add_banya_router)
    dp.include_routers(add_transfer_router)
    await dp.start_polling(tgbot)


if __name__ == '__main__':
    asyncio.run(main())