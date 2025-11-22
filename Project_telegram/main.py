import logging
import asyncio
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from Project_telegram.core.model.helper_db import db_helper_conn
from Project_telegram.core.config import setting
from Project_telegram.api.handlers import router


@asynccontextmanager
async def lifespan():
    try:
        yield
    finally:
        await db_helper_conn.dispose()


async def main() -> None:
    async with lifespan(None):
        bot = Bot(
            token=setting.t_bot.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(router=router)

        await bot.delete_webhook(drop_pending_updates=True)

        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
