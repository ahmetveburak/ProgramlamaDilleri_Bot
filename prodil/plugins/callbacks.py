from pyrogram import filters, Client
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from functools import partial
from prodil.BotConfig import ProDil
from prodil.utils.helpers import make_buttons, save_user, questions
from prodil.utils.queries import QueryHistory
from prodil.utils.myfilters import (
    plang_filter,
    level_filter,
    local_filter,
    resource_filter,
    plang,
    common,
)

command = partial(filters.command, prefixes="/")
history = QueryHistory()


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

    history.add_user(callback.from_user.id)

    await callback.edit_message_text(text=question, reply_markup=InlineKeyboardMarkup(buttons))


@ProDil.on_callback_query(common)
async def common_ts(client: Client, callback: CallbackQuery):
    question = questions.resources["ask"]
    answers = questions.resources["ans"]
    buttons = make_buttons(answers=answers.items(), size=1, back="p_lang")

    question = f"__Bu kategorideki kaynaklar henüz alanına ayrılmamış veya bir dile ait olmayan farklı konulardan kaynaklar içermektedir.__\n\n{question}"

    if callback.data != "resources":
        history.add_data(callback.from_user.id, "p_lang", callback.data)
    if callback.data == "resources":
        history.go_back(callback.from_user.id, "p_lang")

    await callback.edit_message_text(text=question, reply_markup=InlineKeyboardMarkup(buttons))


@ProDil.on_callback_query(plang_filter)
async def ask_level(client: Client, callback: CallbackQuery):
    question = questions.level["ask"]
    answers = questions.level["ans"]
    buttons = make_buttons(answers=answers.items(), size=1, back="p_lang")

    if callback.data != "level":
        history.add_data(callback.from_user.id, "p_lang", callback.data)
    if callback.data == "level":
        history.go_back(callback.from_user.id, "level")

    langs = questions.p_lang["ans"]
    selected_lang = history.hist[callback.from_user.id]["query"]["p_lang"][0]
    await callback.edit_message_text(
        text=f"{langs[selected_lang]} {question}",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@ProDil.on_callback_query(level_filter)
async def ask_local(client: Client, callback: CallbackQuery):
    question = questions.lang["ask"]
    answers = questions.lang["ans"]
    buttons = make_buttons(answers=answers.items(), size=1, back="level")

    if callback.data != "lang":
        history.add_data(callback.from_user.id, "level", callback.data)
    if callback.data == "lang":
        history.go_back(callback.from_user.id, "lang")

    await callback.edit_message_text(
        text=question,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@ProDil.on_callback_query(local_filter)
async def ask_resource(client: Client, callback: CallbackQuery):
    question = questions.resources["ask"]
    answers = questions.resources["ans"]

    # Common resources cause disorder to the bot session. Check first choice is Common or not
    back_button = "p_lang" if history.hist[callback.from_user.id]["query"]["p_lang"][0] == "Common" else "resources"
    buttons = make_buttons(answers=answers.items(), size=1, back=back_button)

    if callback.data != "resources":
        history.add_data(callback.from_user.id, "lang", callback.data)
    if callback.data == "resources":
        history.go_back(callback.from_user.id, "res")

    await callback.edit_message_text(
        text=question,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@ProDil.on_callback_query(resource_filter)
async def send_texts(client: Client, callback: CallbackQuery):
    from_user = callback.from_user
    tags = history.tags(from_user.id)
    history.add_data(from_user.id, "res", callback.data)

    result = history.get_res(from_user.id, tags)
    history.show_history(callback.from_user.id)

    if history.hist[from_user.id]["query"]["res"][0] != "Ebooks":
        save_user(
            from_user=from_user,
            tags=history.hist[from_user.id]["query"],
        )

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

    if (
        msg.chat.id in history.hist.keys()
        and history.hist[msg.chat.id]["query"]["res"][0] == "Ebooks"
        and len(history.hist[msg.chat.id]["download"]) > 0
    ):
        return True
    else:
        return False


###########################################################################
###################### SEND EBOOOOOOOOOOOOKS ##############################
###########################################################################
query_filter = filters.create(lambda _, __, message: query_filter_func(message))


@ProDil.on_message(query_filter & filters.private)
async def send_ebooks(client: Client, message: Message) -> None:
    from_user = message.from_user
    current_chat = message.chat.id

    try:
        books = list(map(int, message.text.split()))
    except ValueError:
        await client.send_message(
            chat_id=current_chat,
            text="Yalnizca sayi dokuman numaralarini bosluk birakarak yaziniz. Or: 1 3 6",
        )
        return

    resources = history.hist[current_chat]["download"]

    down_books = []
    not_in_list = False
    for i in books:
        num = i - 1
        if 0 <= num < len(resources):
            down_books.append(resources[num].name)
            await client.send_cached_media(chat_id=current_chat, file_id=resources[num].file_id)
        else:
            not_in_list = True

    if not_in_list:
        await client.send_message(
            chat_id=current_chat,
            text="Girmis oldugunuz bazi degerler liste sinirlari disinda oldugu icin gonderilememistir.",
        )

    save_user(
        from_user=from_user,
        tags=history.hist[from_user.id]["query"],
        books=[book.name for book in history.hist[from_user.id]["download"]],
    )

    await client.send_message(
        chat_id=current_chat,
        text="Kaynakların Faydalı olması dileğiyle..",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Geri", callback_data="resources")],
                [InlineKeyboardButton(text="Baştan Başla", callback_data="p_lang")],
            ]
        ),
    )

    # tekrar numara gonderildiginde kaynak gondermeyi engellemek icin
    # kaynaklar gonderildikten sonra listeyi temizle
    history.hist[current_chat]["download"].clear()
