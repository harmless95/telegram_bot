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


@router.callback_query(SwitchButton.filter(), StateFilter(Form))
async def switch_buttons(
    call: CallbackQuery, callback_data: SwitchButton, state: FSMContext
):
    if callback_data.button == "Раздел развлечений":
        text, markup = await button_entertainment()
        await state.set_state(Form.button_one)
        await call.message.edit_text(text=text, reply_markup=markup)

    elif callback_data.button == "Учебный раздел":
        text, markup = await button_training()
        await state.set_state(Form.button_two)
        await call.message.edit_text(text=text, reply_markup=markup)

    elif callback_data.button == "главное меню":
        text, markup = await button_main_menu()

        await state.set_state(Form.button_menu)
        await call.message.edit_text(text=text, reply_markup=markup)
    await call.answer()


@router.message()
async def message_handler(message: Message) -> None:
    await message.answer(f"Твой ID: {message.from_user.id}")
