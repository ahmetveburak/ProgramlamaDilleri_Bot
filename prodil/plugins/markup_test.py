from functools import partial

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, Message

from prodil.BotConfig import ProDil
from prodil.utils.botuser import UserNavigation, user_list
from prodil.utils.quest import content_buttons
from prodil_client.client import api

command = partial(filters.command, prefixes="/")


@ProDil.on_message(command("tester"))
async def tester(client: Client, message: Message):
    user = UserNavigation(message.from_user)
    user_list[user.id] = user

    response = user.respons[user.page] = api.get_resources("", "", "", "", user.page)
    text = user.parse_response()
    buttons = content_buttons(len(response["results"]))
    buttons.extend(user.get_buttons(response))

    await client.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
    )
