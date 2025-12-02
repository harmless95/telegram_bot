from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from core.model import SwitchButton, Form

router = Router()


@router.message(Command("Menu"))
async def button_menu(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    # Настройки для самой кнопки
    builder.button(
        text="Перейти к меню", callback_data=SwitchButton(button="главное меню").pack()
    )
    builder.adjust(2)
    markup = builder.as_markup()
    # Состояние что бы бот понимал где он находится
    await state.set_state(state=Form.button_three)
    # Сообщение которое получит пользователь
    await message.answer(text="В главное меню", reply_markup=markup)
