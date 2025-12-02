from aiogram import Router
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import Command
from aiogram.types import (
    Message,
    KeyboardButtonRequestUsers,
    KeyboardButtonRequestChat,
    KeyboardButtonPollType,
)
from aiogram.fsm.context import FSMContext

from core.model import Form

router = Router()


@router.message(Command("help_1"))
async def get_help_keyboard(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.button(text="/button")
    builder.button(text="/start_ai")
    builder.button(
        text="Пользователь",
        request_users=KeyboardButtonRequestUsers(request_id=1, user_is_premium=True),
    )
    builder.button(
        text="чат",
        request_chat=KeyboardButtonRequestChat(
            request_id=2,
            chat_is_channel=False,
            chat_is_forum=True,
        ),
    )
    builder.button(text="контакт", request_contact=True)
    builder.button(text="Локация", request_location=True)
    builder.button(text="Опросник", request_poll=KeyboardButtonPollType(type="regular"))
    builder.button(
        text="Опросник викторина", request_poll=KeyboardButtonPollType(type="quiz")
    )
    builder.adjust(1)

    markup = builder.as_markup()
    await state.set_state(state=Form.button_help_reply)
    await message.answer(text="Проверка выдвижных кнопок", reply_markup=markup)
