from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    button_menu = State()
    button_one = State()
    button_two = State()
    button_three = State()
    button_help_reply = State()
