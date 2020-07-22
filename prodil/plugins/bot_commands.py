from functools import partial
from pyrogram import Filters, Message, Client, CallbackQuery
from pyrogram import InlineKeyboardButton, InlineKeyboardMarkup
from prodil.BotConfig import ProDil

command = partial(Filters.command, prefixes="/")


@ProDil.on_message(command("hakkinda") & Filters.private)
async def test(client: Client, message: Message):

    await client.send_message(
        chat_id=message.chat.id,
        text="Bu bot kâr amacı güdülmeksizin, faydalı olabilecek kaynakların kolayca ulaşılabilir olması için geliştirilmiştir. Burada bulunmasının iyi olacağını düşündüğünüz kaynaklar var ise geliştiricilere iletebilirsiniz.\n\n__Mühendis Köyü kanalımıza katılabilirsiniz.__",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "@musaitbiyerde", url="https://t.me/musaitbiyerde"
                    ),
                    InlineKeyboardButton("@tayyizaman", url="https://t.me/tayyizaman"),
                ],
                [
                    InlineKeyboardButton(
                        "Mühendis Köyü", url="https://t.me/koyumuhendis"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Kaynak Kodlar",
                        url="https://github.com/ahmetveburak/ProgramlamaDilleri",
                    )
                ],
            ]
        ),
    )


@ProDil.on_message(command("oneri") & Filters.private)
async def new_suggestion(client: Client, message: Message):

    await client.send_message(
        chat_id=message.chat.id,
        text="Kaynak önerisinde bulunmak için kaynak formunu doldurarak yeni kaynak önerisinde bulunabilirsin. Önereceğin kaynaklar en kısa zamanda listeye eklenecektir. Botu gelişmesinde katkıda bulunduğun için teşekkür ederiz.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Kaynak Ekleme Formu", url="https://forms.gle/bgoVUXKU81d1Cj5y6"
                    ),
                ],
            ]
        ),
    )
