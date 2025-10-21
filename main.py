import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

import config
from api.handlers import router

loger = logging.getLogger(__name__)

async def main() -> None:
    loger.warning("11")
    bot = Bot(token=config.BOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    loger.warning("22")
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router=router)
    loger.warning("33")
    # await bot.delete_webhook(drop_pending_updates=True)
    # loger.warning("44")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    loger.warning("55")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
