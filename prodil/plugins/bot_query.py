import asyncio

from pyrogram import Client
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, Message, ReplyKeyboardRemove

from prodil.BotConfig import ProDil
from prodil.utils.botuser import UserNavigation, user_list
from prodil.utils.filters import bot_filters
from prodil.utils.helpers import button_toggle, command, user_not_exists
from prodil.utils.quest import content_buttons, make_buttons, quest
from prodil.utils.messages import Text

# TODO refactor repeated lines


@ProDil.on_message(command("start"))
async def start(client: Client, message: Message):
    user = UserNavigation(message.from_user)
    user_list[user.id] = user

    question, answer = quest.get_choices(quest.CATEGORY)
    buttons = make_buttons(answer=answer, size=3, back=False)

    await client.send_message(
        chat_id=message.chat.id,
        text=Text.WELCOME % {"first_name": message.from_user.first_name},
        reply_markup=ReplyKeyboardRemove(True),
    )

    await client.send_message(
        chat_id=message.chat.id,
        text=question,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@ProDil.on_callback_query(bot_filters.category)
async def query_category(_: Client, callback: CallbackQuery):
    user = user_list.get(callback.from_user.id)
    if not user:
        await user_not_exists(callback)
        return

    user.action(callback.data)

    question, answer = quest.get_choices(quest.CATEGORY)
    buttons = make_buttons(answer=answer, size=3, back=False)

    await callback.edit_message_text(text=question, reply_markup=InlineKeyboardMarkup(buttons))


@ProDil.on_callback_query(bot_filters.local)
async def query_local(client: Client, callback: CallbackQuery):
    user = user_list.get(callback.from_user.id)

    if user.start:
        await client.delete_messages(chat_id=callback.message.chat.id, message_ids=(callback.message.message_id - 1,))
        user.start = False

    if not user:
        await user_not_exists(callback)
        return

    user.action(callback.data, quest.CATEGORY)

    question, answer = quest.get_choices(quest.LOCAL)
    buttons = make_buttons(answer=answer, size=1, back=quest.CATEGORY)

    await callback.edit_message_text(
        text=question,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@ProDil.on_callback_query(bot_filters.content)
async def query_content(_: Client, callback: CallbackQuery):
    user = user_list.get(callback.from_user.id)
    if not user:
        await user_not_exists(callback)
        return

    user.action(callback.data, quest.LOCAL)

    question, answer = quest.get_choices(quest.CONTENT)
    buttons = make_buttons(answer=answer, size=1, back=quest.LOCAL)

    await callback.edit_message_text(
        text=question,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@ProDil.on_callback_query(bot_filters.connection)
async def query_connection(_: Client, callback: CallbackQuery):
    user = user_list.get(callback.from_user.id)
    if not user:
        await user_not_exists(callback)
        return

    user.action(callback.data, quest.CONTENT)

    user.set_page_data(callback.message.reply_markup.inline_keyboard)
    response = user.get_resources()

    buttons = content_buttons(len(response["results"])) if callback.data == "DC" else []
    buttons.extend(user.get_buttons(response))

    text = user.parse_response()
    if text:
        await callback.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )

    else:
        await callback.answer(
            text=Text.NO_RESOURCE,
            show_alert=True,
        )


@ProDil.on_callback_query(bot_filters.numbers)
async def query_numbers(_: Client, callback: CallbackQuery):
    user = user_list.get(callback.from_user.id)
    if not user:
        await user_not_exists(callback)
        return

    selected = int(callback.data) - 1
    x, y = int(selected / 4), int(selected % 4)

    markup = callback.message.reply_markup.inline_keyboard
    button_toggle(markup[x][y])

    await callback.edit_message_text(
        text=callback.message.text,
        reply_markup=callback.message.reply_markup,
        disable_web_page_preview=True,
    )


@ProDil.on_callback_query(bot_filters.change)
async def query_next(_: Client, callback: CallbackQuery):
    user = user_list.get(callback.from_user.id)
    if not user:
        await user_not_exists(callback)
        return

    user.set_page_data(callback.message.reply_markup.inline_keyboard)
    is_next = callback.data == "next"

    if is_next:
        user.page += 1
    else:
        user.page -= 1

    response = user.get_response()
    buttons = user.get_data()
    if user.page - 1 == 1 or not response:
        response = user.get_resources()
        buttons = content_buttons(len(response["results"])) if user.content == "DC" else []
        buttons.extend(user.get_buttons(response))

    await callback.edit_message_text(
        text=user.parse_response(),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True,
    )


@ProDil.on_callback_query(bot_filters.download)
async def query_prev(client: Client, callback: CallbackQuery):
    user = user_list.get(callback.from_user.id)
    user.set_page_data(callback.message.reply_markup.inline_keyboard)

    if not user:
        await user_not_exists(callback)
        return

    for document in user.get_documents():
        failed_docs = []
        try:
            await client.send_cached_media(
                chat_id=user.id,
                file_id=document["file_id"],
            )
        except MediaEmpty as err:
            failed_docs.append(document["name"])
            # TODO LOG
            print(f"{err}: {document['name']} isimli dosya bozuk")

        if len(failed_docs) > 0:
            doc_names = "\n".join(failed_docs)
            await callback.answer(text=Text.ERROR_RESOURCE % {"doc_names": doc_names})

        await asyncio.sleep(5)

    await client.delete_messages(
        chat_id=callback.from_user.id,
        message_ids=[callback.message.message_id],
    )
    # TODO Send This Resources
    del user_list[user.id]

    await client.send_message(
        chat_id=callback.from_user.id,
        text=Text.RESTART,
        reply_markup=ReplyKeyboardRemove(True),
    )
