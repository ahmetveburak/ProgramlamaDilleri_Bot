from functools import partial
from pyrogram import filters, Client
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)

from prodil.BotConfig import ProDil

from prodil.models.model import session, Documents, Links, Books, Questions, Users
from prodil.utils.myfilters import (
    lngFilter,
    lvlFilter,
    lclFilter,
    resFilter,
    plang,
    common,
)
from prodil.utils.helpers import make_buttons
from prodil.utils.queries import History
from datetime import datetime


questions = session.query(Questions).filter(Questions.id == 1).first()
command = partial(filters.command, prefixes="/")
history = History()


@ProDil.on_message(command("start"))
async def start(client: Client, message: Message):
    question = questions.p_lang["ask"]
    answers = questions.p_lang["ans"]
    buttons = make_buttons(answers=answers.items(), size=3, back=False)

    history.add_user(message.chat.id)

    await client.send_message(
        chat_id=message.chat.id,
        text=f"""__Hoşgeldin__ **{message.from_user.first_name}** __, bu bot henüz geliştirme aşamasındadır. Bu sebeple kaynak altyapısı sınırlı seviyededir. Önerebileceğin kaynaklar varsa__ /hakkinda __kısmından bize ulaşabilir, botun kullanımı sırasında bir sorunla karşılaşırsan tekrardan__ /start __komutunu çalıştırabilirsin.__""",
        reply_markup=ReplyKeyboardRemove(True),
    )
    await client.send_message(
        chat_id=message.chat.id,
        text=question,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@ProDil.on_callback_query(plang)
async def ask_lang(client: Client, callback: CallbackQuery):
    question = questions.p_lang["ask"]
    answers = questions.p_lang["ans"]
    buttons = make_buttons(answers=answers.items(), size=3, back=False)

    # history.add_data(callback.from_user.id, callback.data)
    # if callback.data == "p_lang":
    #     history.go_back(callback.from_user.id)
    history.hist[callback.from_user.id]["query"] = []

    await callback.edit_message_text(text=question, reply_markup=InlineKeyboardMarkup(buttons))


@ProDil.on_callback_query(common)
async def common_ts(client: Client, callback: CallbackQuery):
    question = questions.resources["ask"]
    answers = questions.resources["ans"]
    buttons = make_buttons(answers=answers.items(), size=1, back="p_lang")

    question = f"__Bu kategorideki kaynaklar henüz alanına ayrılmamış veya bir dile ait olmayan farklı konulardan kaynaklar içermektedir.__\n\n{question}"
    history.add_data(callback.from_user.id, callback.data)
    if callback.data == "resources":
        history.go_back(callback.from_user.id)

    await callback.edit_message_text(text=question, reply_markup=InlineKeyboardMarkup(buttons))


@ProDil.on_callback_query(lngFilter)
async def ask_level(client: Client, callback: CallbackQuery):
    question = questions.level["ask"]
    answers = questions.level["ans"]
    buttons = make_buttons(answers=answers.items(), size=1, back="p_lang")

    history.add_data(callback.from_user.id, callback.data)
    if callback.data == "level":
        history.go_back(callback.from_user.id)

    langs = questions.p_lang["ans"]
    selected_lang = history.hist[callback.from_user.id]["query"][0]
    await callback.edit_message_text(
        text=f"{langs[selected_lang]} {question}",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@ProDil.on_callback_query(lvlFilter)
async def ask_local(client: Client, callback: CallbackQuery):
    question = questions.lang["ask"]
    answers = questions.lang["ans"]
    buttons = make_buttons(answers=answers.items(), size=1, back="level")

    history.add_data(callback.from_user.id, callback.data)
    if callback.data == "lang":
        history.go_back(callback.from_user.id)

    await callback.edit_message_text(text=question, reply_markup=InlineKeyboardMarkup(buttons))


@ProDil.on_callback_query(lclFilter)
async def ask_resource(client: Client, callback: CallbackQuery):
    question = questions.resources["ask"]
    answers = questions.resources["ans"]
    buttons = make_buttons(answers=answers.items(), size=1, back="lang")

    history.add_data(callback.from_user.id, callback.data)
    if callback.data == "resources":
        history.go_back(callback.from_user.id)

    await callback.edit_message_text(text=question, reply_markup=InlineKeyboardMarkup(buttons))


@ProDil.on_callback_query(resFilter)
async def send_texts(client: Client, callback: CallbackQuery):
    cb = callback.from_user
    history.add_data(cb.id, callback.data)
    history.show_history(cb.id)
    result = history.get_res(cb.id)
    tags = history.tags(cb.id)

    # if tags[-1] == "links" or tags[-1] == "ebooks":

    #     user = Users(
    #         user_id=cb.id,
    #         first_name=cb.first_name,
    #         last_name=cb.last_name if cb.last_name else None,
    #         username=cb.username if cb.username else None,
    #         tags=tags,
    #         books=None,
    #         date=datetime.now(),
    #     )
    #     user.save()

    await callback.edit_message_text(
        text=result,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Geri", callback_data="resources")],
                [InlineKeyboardButton(text="Baştan Başla", callback_data="p_lang")],
            ]
        ),
    )


# @ProDil.on_message(filters.text)
# async def send_ebooks(client: Client, message: Message):
#     msg = message.from_user

#     if message.text == "/hakkinda":
#         # TODO need to fix
#         pass

#     elif msg.id in history.hist.keys():

#         books = message.text.split()
#         tags = history.tags(message.chat.id)
#         resources = history.hist[message.chat.id]["res"]

#         down_books = []

#         for i in books:
#             n = int(i) - 1
#             # print(f"{resources[n].name}\n{resources[n].path}")
#             down_books.append(resources[n].name)
#             await client.send_cached_media(chat_id=message.chat.id, file_id=resources[n].file_id)

#         user = Users(
#             user_id=msg.id,
#             first_name=msg.first_name,
#             last_name=msg.last_name if msg.last_name else None,
#             username=msg.username if msg.username else None,
#             tags=tags,
#             books=down_books,
#             date=datetime.now(),
#         )
#         user.save()

#     await client.send_message(
#         chat_id=message.chat.id,
#         text="Kaynakların Faydalı olması dileğiyle..",
#         disable_web_page_preview=True,
#         reply_markup=InlineKeyboardMarkup(
#             [
#                 [InlineKeyboardButton(text="Geri", callback_data="resources")],
#                 [InlineKeyboardButton(text="Baştan Başla", callback_data="p_lang")],
#             ]
#         ),
#     )
