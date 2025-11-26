from aiogram import Router, html
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


from core.model import SwitchButton, Form, db_helper_conn
from .button_builder import button_main_menu
from .mapping_button import ALL_BUTTON
from .Dependencies import save_db_user
from .text_gpt.file_gpt import text_message

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    async with db_helper_conn.get_generator_session() as session:
        await save_db_user(user_id=message.from_user.id, session=session)
        await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@router.message(Command("Button"))
async def button_message(message: Message, state: FSMContext):
    text, markup = await button_main_menu()
    await state.set_state(Form.button_menu)
    await message.answer(text=text, reply_markup=markup)


@router.message(Command("GPT"))
async def chat_gpt(message: Message):
    result_text = await text_message(message=message)
    await message.answer(text=result_text)


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


@router.message()
async def message_handler(message: Message) -> None:
    await message.answer(f"Твой ID: {message.from_user.id}")
