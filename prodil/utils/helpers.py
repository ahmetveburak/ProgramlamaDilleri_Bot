from pyrogram.types import InlineKeyboardButton
from typing import List


def slicer(button_list: List[InlineKeyboardButton], size: int) -> list:
    return [button_list[i : i + size] for i in range(0, len(button_list), size)]


def make_buttons(answers: dict, size: int, back: str) -> List[InlineKeyboardButton]:
    buttons: list = [InlineKeyboardButton(text=v, callback_data=k) for k, v in answers]
    buttons = slicer(buttons, size)

    if back:
        back_button: InlineKeyboardButton = InlineKeyboardButton(text="Geri", callback_data=back)
        buttons.append([back_button])

    return buttons
