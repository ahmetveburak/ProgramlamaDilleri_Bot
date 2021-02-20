from functools import partial
from pyrogram import filters, Client
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from pyrogram.types.messages_and_media import message

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
    # history.hist[callback.from_user.id]["query"] = []
    history.add_user(callback.from_user.id)

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

    if tags[-1] == "links" or tags[-1] == "books":
        user = session.query(Users).filter(Users.uid == str(cb.id)).first()
        if user:
            if cb.first_name not in user.first_name:
                fn = user.first_name.copy()
                fn.append(cb.first_name)
                user.first_name = fn
            if cb.last_name and cb.last_name not in user.last_name:
                ln = user.last_name.copy()
                ln.append(cb.last_name)
                user.last_name = ln
            if cb.username and cb.username not in user.username:
                un = user.username.copy()
                un.append(cb.username)
                user.username = un

            user_hist = user.history.copy()
            user_hist.update({str(int(datetime.now().timestamp())): {"tags": tags, "books": []}})
            user.history = user_hist
            print("links or books saved")
        else:
            user = Users(
                uid=cb.id,
                first_name=[cb.first_name],
                last_name=[cb.last_name] if cb.last_name else [],
                username=[cb.username] if cb.username else [],
                history={
                    str(int(datetime.now().timestamp())): {"tags": tags, "books": []},
                },
            )
            print("new user")
            session.add(user)
        session.commit()

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


def query_filter_func(msg: Message) -> bool:

    if msg.chat.id in history.hist.keys():
        if history.hist[msg.chat.id]["query"][-1] == "ebooks":
            return True
    else:
        return False


query_filter = filters.create(lambda _, __, message: query_filter_func(message))


@ProDil.on_message(query_filter & filters.private)
async def send_ebooks(client: Client, message: Message):
    msg = message.from_user

    try:
        books = list(map(int, message.text.split()))
    except ValueError:
        await client.send_message(
            chat_id=message.chat.id,
            text="Yalnizca sayi dokuman numaralarini bosluk birakarak yaziniz. Or: 1 3 6",
        )
        return

    tags = history.tags(message.chat.id)
    resources = history.hist[message.chat.id]["res"]

    down_books = []
    in_list = False
    for i in books:
        n = i - 1
        if 0 <= n < len(resources):
            # print(f"{resources[n].name}\n{resources[n].path}")
            down_books.append(resources[n].name)
            # print(resources[n].name)
            await client.send_cached_media(chat_id=message.chat.id, file_id=resources[n].file_id)
        else:
            in_list = True

    if in_list:
        await client.send_message(
            chat_id=message.chat.id,
            text="Girmis oldugunuz bazi degerler liste sinirlari disinda oldugu icin gonderilememistir.",
        )

    user = session.query(Users).filter(Users.uid == str(msg.id)).first()
    if user:
        if msg.first_name not in user.first_name:
            fn = user.first_name.copy()
            fn.append(msg.first_name)
            user.first_name = fn
        if msg.last_name and msg.last_name not in user.last_name:
            ln = user.last_name.copy()
            ln.append(msg.last_name)
            user.last_name = ln
        if msg.username and msg.username not in user.username:
            un = user.username.copy()
            un.append(msg.username)
            user.username = un

        user_hist = user.history.copy()
        user_hist.update(
            {str(int(datetime.now().timestamp())): {"tags": tags, "books": down_books}}
        )
        user.history = user_hist

    else:
        user = Users(
            uid=msg.id,
            first_name=[msg.first_name],
            last_name=[msg.last_name] if msg.last_name else [],
            username=[msg.username] if msg.username else [],
            history={
                str(int(datetime.now().timestamp())): {"tags": tags, "books": down_books},
            },
        )

        session.add(user)
    session.commit()

    await client.send_message(
        chat_id=message.chat.id,
        text="Kaynakların Faydalı olması dileğiyle..",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Geri", callback_data="resources")],
                [InlineKeyboardButton(text="Baştan Başla", callback_data="p_lang")],
            ]
        ),
    )
