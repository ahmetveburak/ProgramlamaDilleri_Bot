from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from prodil.BotConfig import ProDil
from prodil.utils.helpers import command


@ProDil.on_message(command("hakkinda") & filters.private)
async def test(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id,
        text=(
            "Bu bot kâr amacı güdülmeksizin, faydalı olabilecek kaynakların "
            "kolayca ulaşılabilir olması için geliştirilmiştir. "
            "Burada bulunmasının iyi olacağını düşündüğünüz "
            "kaynaklar var ise geliştiricilere iletebilirsiniz."
            "\n\n__Mühendis Köyü kanalımıza katılabilirsiniz.__"
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("@musaitbiyerde", url="https://t.me/musaitbiyerde"),
                ],
                [InlineKeyboardButton("Mühendis Köyü", url="https://t.me/koyumuhendis")],
                [
                    InlineKeyboardButton(
                        "Kaynak Kodlar",
                        url="https://github.com/ahmetveburak/ProgramlamaDilleri",
                    )
                ],
            ]
        ),
    )
