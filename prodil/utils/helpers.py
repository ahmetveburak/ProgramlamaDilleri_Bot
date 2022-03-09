from functools import partial

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton

from prodil.utils import USERS

command = partial(filters.command, prefixes="/")


def button_toggle(button: InlineKeyboardButton) -> None:
    is_selected = button.text[0] == "🔴"

    if is_selected:
        button.text = button.text.replace("🔴", "🟢")
    else:
        button.text = button.text.replace("🟢", "🔴")


async def user_not_exists(callback):
    await callback.answer(
        text="Oturumunuz sonlandirildi. /start ile bastan baslayin.",
        show_alert=True,
    )


async def check_user(_, __, query):
    user = USERS.get(query.from_user.id)
    if not user:
        await user_not_exists(query)
        return False
    return True


is_active_user = filters.create(check_user)
