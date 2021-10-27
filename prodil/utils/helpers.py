from pyrogram.types import InlineKeyboardButton
from pyrogram import filters
from functools import partial

command = partial(filters.command, prefixes="/")


def button_toggle(button: InlineKeyboardButton) -> None:
    is_selected = button.text[0] == "🔴"

    if is_selected:
        button.text = button.text.replace("🔴", "🟢")
    else:
        button.text = button.text.replace("🟢", "🔴")
