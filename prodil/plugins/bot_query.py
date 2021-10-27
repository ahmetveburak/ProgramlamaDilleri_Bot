from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, Message, ReplyKeyboardRemove

from prodil.BotConfig import ProDil
from prodil.utils.botuser import UserNavigation, user_list
from prodil.utils.filters import bot_filters
from prodil.utils.helpers import button_toggle, command
from prodil.utils.quest import content_buttons, make_buttons, quest
from prodil_client.client import api


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


@ProDil.on_callback_query(bot_filters.downloads)
async def query_send_book(_: Client, callback: CallbackQuery):
    print(callback.from_user.first_name, "\n", callback.from_user.id)
    user = user_list.get(callback.from_user.id)
    user.action(callback.data, quest.CONTENT)

    user.set_page_data(callback.message.reply_markup.inline_keyboard)

    response = user.respons[user.page] = api.get_resources(**user.query_args)

    buttons = content_buttons(len(response["results"])) if callback.data == "DC" else []
    buttons.extend(user.get_buttons(response, callback.data == "DC"))

    text = user.parse_response()
    if text:
        await callback.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    else:
        await callback.answer(
            text="Bu alanda henuz kaynak bulunmamaktadir.",
            show_alert=True,
        )


@ProDil.on_callback_query(bot_filters.numbers)
async def query_numbers(_: Client, callback: CallbackQuery):
    selected = int(callback.data) - 1
    x, y = int(selected / 4), int(selected % 4)

    markup = callback.message.reply_markup.inline_keyboard
    button_toggle(markup[x][y])

    await callback.edit_message_text(
        text=callback.message.text,
        reply_markup=callback.message.reply_markup,
    )


@ProDil.on_callback_query(bot_filters.change)
async def query_next(_: Client, callback: CallbackQuery):
    user = user_list[callback.from_user.id]
    user.set_page_data(callback.message.reply_markup.inline_keyboard)
    is_next = callback.data == "next"

    if is_next:
        user.page += 1
    else:
        user.page -= 1

    response = user.get_response()
    buttons = user.get_data()
    if not response:
        response = user.respons[user.page] = api.get_resources(**user.query_args)
        buttons = content_buttons(len(response["results"]))
        buttons.extend(user.get_buttons(response))

    await callback.edit_message_text(
        text=user.parse_response(),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@ProDil.on_callback_query(bot_filters.download)
async def query_prev(client: Client, callback: CallbackQuery):
    user = user_list[callback.from_user.id]

    await client.delete_messages(
        chat_id=callback.from_user.id,
        message_ids=[callback.message.message_id],
    )
    # TODO Send This Resources
    user.get_resources()
    del user_list[user.id]

    await client.send_message(
        chat_id=callback.from_user.id,
        text="text /startt",
        reply_markup=ReplyKeyboardRemove(True),
    )
