from typing import List, Dict

import logging
from aiogram import Router, html, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.config import setting
from core.model import SwitchButton, Form, db_helper_conn
from .button_builder import button_main_menu
from .mapping_button import ALL_BUTTON
from .Dependencies import save_db_user

from .button_default.command_gpt import command_hand, command_stop, message_sent

# ✅ Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()
user_history: Dict[int, List[dict]] = {}
user_disabled: set[int] = set()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    async with db_helper_conn.get_generator_session() as session:
        await save_db_user(user_id=message.from_user.id, session=session)
        await message.answer(
            f"Hello, {html.bold(message.from_user.full_name)}!\n"
            f"📱 ID: <code>{message.from_user.id}</code>"
        )


@router.message(Command("button"))
async def button_message(message: Message, state: FSMContext):
    text, markup = await button_main_menu()
    await state.set_state(Form.button_menu)
    await message.answer(text=text, reply_markup=markup)


@router.message(Command("start_ai"))
async def chat_gpt(message: Message):
    async with db_helper_conn.get_generator_session() as session:
        await command_hand(message=message, session=session)


@router.message(Command("stop_ai"))
async def stop_bot_for_user(message: Message):
    async with db_helper_conn.get_generator_session() as session:
        await command_stop(message=message, session=session)


@router.message(Command("help"))
async def help_handler(message: Message):
    commands_help = setting.t_bot.commands
    help_text = "📋 Доступные команды:\n\n"
    for command in commands_help:
        help_text += f"• /{command[0]} - {command[1]}\n"
    await message.answer(text=help_text)


@router.message(F.text & ~F.text.startswith("/"))
async def groq_chat(message: Message):
    async with db_helper_conn.get_generator_session() as session:
        await message_sent(message=message, session=session)


@router.callback_query(SwitchButton.filter(), StateFilter(Form))
async def switch_buttons(
    call: CallbackQuery, callback_data: SwitchButton, state: FSMContext
):
    handler = ALL_BUTTON.get(callback_data.button)
    if handler:
        await handler(call=call, state=state)
        await call.answer()
    else:
        await call.answer(text="Неизвестная команда", show_alert=True)


#
# @router.message()
# async def message_handler(message: Message) -> None:
#     """Обработчик неизвестных команд"""
#     await message.answer(
#         f"❓ Неизвестная команда\n"
#         f"📱 Твой ID: <code>{message.from_user.id}</code>\n"
#         f"🔗 /help — Доступные команды"
#     )
