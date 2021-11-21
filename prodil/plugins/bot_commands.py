import asyncio

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from prodil.BotConfig import ProDil, api
from prodil.utils.helpers import command


@ProDil.on_message(command("hakkinda") & filters.private)
async def bot_about(client: Client, message: Message):
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


@ProDil.on_message(filters.me & filters.media & filters.private)
async def bot_file_update(_: Client, message: Message):
    update = api.update_resource(
        file_name=message.document.file_name,
        file_size=message.document.file_size,
        file_id=message.document.file_id,
    )

    text = "Dosya guncellenemedi."
    if update.status_code == 200:
        text = "Dosya basariyla guncellendi"

    reply_message = await message.reply_text(text=f"`{text}`")
    await asyncio.sleep(3)
    await reply_message.delete()
