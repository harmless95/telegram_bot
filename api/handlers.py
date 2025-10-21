from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@router.message()
async def message_handler(message: Message) -> None:
    await message.answer(f"Твой ID: {message.from_user.id}")