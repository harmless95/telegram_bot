from aiogram import Router, html
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


from Project_telegram.core.model.callback_data import SwitchButton
from Project_telegram.core.model.States_button import Form
from .button_builder import button_main_menu
from .mapping_button import ALL_BUTTON

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
    handler = ALL_BUTTON.get(callback_data.button)
    if handler:
        await handler(call=call, state=state)
        await call.answer()
    else:
        await call.answer(text="Неизвестная команда", show_alert=True)


@router.message()
async def message_handler(message: Message) -> None:
    await message.answer(f"Твой ID: {message.from_user.id}")
