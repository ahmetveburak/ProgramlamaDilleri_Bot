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


@ProDil.on_callback_query(bot_filters.common)
async def common_ts(_: Client, callback: CallbackQuery):
    question, answer = quest.get_choices(quest.CONTENT)
    buttons = make_buttons(answer=answer, size=1, back="p_lang")

    question = (
        f"__Bu kategorideki kaynaklar henüz alanına ayrılmamış "
        f"veya bir dile ait olmayan farklı konulardan kaynaklar "
        f"içermektedir.__\n\n{question}"
    )

    # if callback.data != "resources":
    #     history.add_data(callback.from_user.id, "p_lang", callback.data)
    # if callback.data == "resources":
    #     history.go_back(callback.from_user.id, "p_lang")

    await callback.edit_message_text(text=question, reply_markup=InlineKeyboardMarkup(buttons))


@ProDil.on_callback_query(bot_filters.level)
async def query_level(_: Client, callback: CallbackQuery):
    user = user_list.get(callback.from_user.id)
    user.action(callback.data, quest.CATEGORY)

    question, answer = quest.get_choices(quest.LEVEL)
    buttons = make_buttons(answer=answer, size=1, back=quest.CATEGORY)

    await callback.edit_message_text(
        text=f"**{user.category}** {question}",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@ProDil.on_callback_query(bot_filters.local)
async def query_local(_: Client, callback: CallbackQuery):
    user = user_list.get(callback.from_user.id)
    user.action(callback.data, quest.LEVEL)

    question, answer = quest.get_choices(quest.LOCAL)
    buttons = make_buttons(answer=answer, size=1, back=quest.LEVEL)

    # if callback.data != "lang":
    #     history.add_data(callback.from_user.id, "level", callback.data)
    # if callback.data == "lang":
    #     history.go_back(callback.from_user.id, "lang")

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

    # Common resources cause disorder to the bot session. Check first choice is Common or not
    # back_button = "p_lang" if history.hist[callback.from_user.id]["query"]["p_lang"][0] == "Common" else "resources"
    # buttons = make_buttons(answers=answers.items(), size=1, back=back_button)

    # if callback.data != "resources":
    #     history.add_data(callback.from_user.id, "lang", callback.data)
    # if callback.data == "resources":
    #     history.go_back(callback.from_user.id, "res")

    await callback.edit_message_text(
        text=question,
        reply_markup=InlineKeyboardMarkup(buttons),
    )
