from aiogram import Router, html
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


from core.model.callback_data import SwitchButton
from core.model.States_button import Form
from .button_hadler import button_main_menu, button_entertainment, button_training

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@router.message(Command("Button"))
async def button_message(message: Message, state: FSMContext):
    text, markup = await button_main_menu()
    await state.set_state(Form.button_menu)
    await message.answer(text=text, reply_markup=markup)


@router.message()
async def message_handler(message: Message) -> None:
    await message.answer(f"Твой ID: {message.from_user.id}")