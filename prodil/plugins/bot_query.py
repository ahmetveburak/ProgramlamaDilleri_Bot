from functools import partial
from typing import Dict

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, Message, ReplyKeyboardRemove

from prodil.BotConfig import ProDil
from prodil.utils.botuser import UserNavigation
from prodil.utils.filters import bot_filters
from prodil.utils.quest import make_buttons, quest

command = partial(filters.command, prefixes="/")

user_list: Dict[int, UserNavigation] = {}


@ProDil.on_message(command("start"))
async def start(client: Client, message: Message):
    user = UserNavigation(message.from_user)
    user_list[user.id] = user

    question, answer = quest.get_choices(quest.CATEGORY)
    buttons = make_buttons(answer=answer, size=3, back=False)

    await client.send_message(
        chat_id=message.chat.id,
        text=f"__Hoşgeldin__ **{message.from_user.first_name}** __, "
        f"bu bot henüz geliştirme aşamasındadır. "
        f"Bu sebeple kaynak altyapısı sınırlı seviyededir. "
        f"Önerebileceğin kaynaklar varsa__ /hakkinda __kısmından bize ulaşabilir, "
        f"botun kullanımı sırasında bir sorunla karşılaşırsan tekrardan"
        f"__ /start __komutunu çalıştırabilirsin.__",
        reply_markup=ReplyKeyboardRemove(True),
    )

    await client.send_message(
        chat_id=message.chat.id,
        text=question,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@ProDil.on_callback_query(bot_filters.start)
async def query_start(_: Client, callback: CallbackQuery):
    user = user_list.get(callback.from_user.id)
    user.action(callback.data)

    question, answer = quest.get_choices(quest.CATEGORY)
    buttons = make_buttons(answer=answer, size=3, back=False)

    await callback.edit_message_text(text=question, reply_markup=InlineKeyboardMarkup(buttons))


@ProDil.on_callback_query(bot_filters.level)
async def query_level(_: Client, callback: CallbackQuery):
    user = user_list.get(callback.from_user.id)
    user.action(callback.data, quest.CATEGORY)

    question, answer = quest.get_choices(quest.LEVEL)
    buttons = make_buttons(answer=answer, size=1, back=quest.CATEGORY)

    await callback.edit_message_text(
        text=question,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@ProDil.on_callback_query(bot_filters.local)
async def query_local(_: Client, callback: CallbackQuery):
    user = user_list.get(callback.from_user.id)
    user.action(callback.data, quest.LEVEL)

    question, answer = quest.get_choices(quest.LOCAL)
    buttons = make_buttons(answer=answer, size=1, back=quest.LEVEL)

    await callback.edit_message_text(
        text=question,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@ProDil.on_callback_query(bot_filters.content)
async def query_content(_: Client, callback: CallbackQuery):
    user = user_list.get(callback.from_user.id)
    user.action(callback.data, quest.LOCAL)

    question, answer = quest.get_choices(quest.CONTENT)
    buttons = make_buttons(answer=answer, size=1, back=quest.LOCAL)

    await callback.edit_message_text(
        text=question,
        reply_markup=InlineKeyboardMarkup(buttons),
    )
