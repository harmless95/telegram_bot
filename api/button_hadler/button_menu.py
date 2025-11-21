from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from core.model.callback_data import SwitchButton


async def button_main_menu() -> tuple[str, InlineKeyboardMarkup]:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="вк",
        url="https://vk.com/audios150453702?q=%D0%B1%D1%80%D0%B0%D1%82%D1%8C%D1%8F%20%D0%B3%D1%80%D0%B8%D0%BC",
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
