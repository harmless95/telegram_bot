from aiogram.filters.callback_data import CallbackData


class SwitchButton(CallbackData, prefix="switch"):
    button: str
