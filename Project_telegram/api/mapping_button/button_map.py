from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from Project_telegram.api.button_builder import (
    button_entertainment,
    button_training,
    button_main_menu,
)
from Project_telegram.core.model.States_button import Form


async def handler_entertainment(call: CallbackQuery, state: FSMContext):
    text, markup = await button_entertainment()
    await state.set_state(Form.button_one)
    await call.message.edit_text(text=text, reply_markup=markup)


async def handler_button_training(call: CallbackQuery, state: FSMContext):
    text, markup = await button_training()
    await state.set_state(Form.button_two)
    await call.message.edit_text(text=text, reply_markup=markup)


async def handler_main_menu(call: CallbackQuery, state: FSMContext):
    text, markup = await button_main_menu()

    await state.set_state(Form.button_menu)
    await call.message.edit_text(text=text, reply_markup=markup)


ALL_BUTTON = {
    "Раздел развлечений": handler_entertainment,
    "Учебный раздел": handler_button_training,
    "главное меню": handler_main_menu,
}
