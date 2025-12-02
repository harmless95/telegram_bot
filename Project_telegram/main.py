import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import setting
from api.handlers import router
from api.example_practice.new_router import router as router_example
from api.example_practice.practice_replay_keyboard import router as router_reply

loger = logging.getLogger(__name__)


async def main() -> None:
    loger.warning("TOKEN: %s", setting.t_bot.token)
    bot = Bot(
        token=setting.t_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router=router)
    dp.include_router(router=router_example)
    dp.include_router(router=router_reply)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
