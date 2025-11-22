from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from Project_telegram.core.model.callback_data import SwitchButton


async def button_training() -> tuple[str, InlineKeyboardMarkup]:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Предыдущий раздел",
        callback_data=SwitchButton(button="Раздел развлечений").pack(),
    )
    builder.button(text="tw", url="https://www.twitch.tv")
    builder.button(
        text="главное меню",
        callback_data=SwitchButton(button="главное меню").pack(),
    )
    builder.adjust(2)
    markup = builder.as_markup()
    return "Учебный раздел", markup
