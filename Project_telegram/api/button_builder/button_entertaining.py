from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from core.model import SwitchButton


async def button_entertainment() -> tuple[str, InlineKeyboardMarkup]:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Следующий раздел",
        callback_data=SwitchButton(button="Учебный раздел").pack(),
    )
    builder.button(text="anime", url="https://v17.astar.bz/anime/page/2/")
    builder.button(
        text="главное меню",
        callback_data=SwitchButton(button="главное меню").pack(),
    )
    builder.adjust(2)
    markup = builder.as_markup()
    return "Развлекательный раздел", markup
