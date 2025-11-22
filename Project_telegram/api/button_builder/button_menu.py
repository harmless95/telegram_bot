from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from Project_telegram.core.model.callback_data import SwitchButton


async def button_main_menu() -> tuple[str, InlineKeyboardMarkup]:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="вк",
        url="https://vk.com/feed",
    )
    builder.button(
        text="youtube",
        url="https://www.youtube.com/",
    )
    builder.button(
        text="Следующий раздел",
        callback_data=SwitchButton(button="Раздел развлечений").pack(),
    )
    builder.adjust(2)
    markup = builder.as_markup()
    return "Меню", markup
