from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode

from config import API_KEY

storage = MemoryStorage()
tgbot = Bot(token=API_KEY, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage)


@dp.shutdown()
async def on_shutdown():
    await tgbot.close()
    # await dp.close()


@dp.startup()
async def on_startup():
    await tgbot.delete_webhook(drop_pending_updates=True)